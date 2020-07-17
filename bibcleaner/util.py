import argparse
import sys
import flask
import os
import re
import time
import json
import pdb
import random
import tempfile
import traceback
from collections import *

import click
import biblib.bib
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.pool import NullPool




# synonyms are reconciled to the dictionary key.  The list of synonyms is listed in priority order
# e.g., all journal and article entry keys are renamed into booktitle keys
synonyms = dict(
    booktitle=['booktitle', 'journal', 'article', 'publisher']
)

# These constitute "real" article entries.  
# We normalize them all into @inproceedings entries
entry_types = set(['inproceedings', 'article', 'journal'])

# keys part of inproceedings/journal/article entries, skip all others
entry_keys = ['author', 'title', 'journal', 'booktitle', 'year', 'url', 'publisher']

# throw away all other entry keys, if you change this, make sure to change the entries schema in the 
# create table statement below.
allowed_keys = ['type', 'key', 'title', 'year', 'booktitle', 'author', 'howpublished', 'publisher', 'url']







# setup database

SETUPQS = ["""CREATE TABLE if not exists mapping (
  id serial,
  oldbook text,
  newbook text
);""",
"""CREATE TABLE if not exists entries (
  id serial,
  type text NOT NULL, -- book, misc, or inproceedings
  key text UNIQUE NOT NULL,  -- wu2015
  title text NOT NULL,
  year text,
  booktitle text, -- old book titel
  author text,
  howpublished text,
  publisher text,
  url text
)
""",
"""CREATE TABLE if not exists files (
  name text
)""",
"""CREATE TABLE if not exists file_entries (
  fid int references files(rowid),
  eid int references entries(rowid)
)"""
]

DATABASEURI = "sqlite:///bibcleaner.db"

engine = create_engine(DATABASEURI)
for q in SETUPQS:
  engine.execute(q)




def fix_synonyms(fields, synonyms):
  for key in synonyms:
    for syn in synonyms[key]:

      # find the synonym in fields
      found = False
      for field in fields:
        if syn == field.lower() and fields[field]:
          fields[key] = fields.get(field)
          if key != field:
            del fields[field]
          found = True
          break
      if found: break
  return fields


def tuple_to_entry(keys, row):
  # turn tuples into biblib.bib.Entry objects
  if row['type'] not in entry_types:
    if 'key' not in keys:
      keys = keys + ['key']
  d = dict([(key, str(row[key])) for key in keys if row[key]])
  ent = biblib.bib.Entry(d.items())
  ent.typ = row['type']
  ent.key = row['key']
  return ent

def sql_to_entries(q, args=()):
  print(q)
  #print(" ".join(q.split("\n")))

  # turn tuples into biblib.bib.Entry objects
  ents = []
  cur = engine.execute(q, args)
  keys = cur.keys()
  list(map(keys.remove, ['type', 'key']))
  for row in cur:
    ents.append(tuple_to_entry(keys, row))
  return ents






def load_bibfile(bibfile, min_crossrefs=None):
  """
  Given bib file object, parse it and return the list of Entry objects
  Normalizes all inproceedings, article, and journal entry types to inproceedings type.
  """
  try:
    # Load databases
    # Parser used to take "paranoid=False" as input
    db = biblib.bib.Parser().parse(bibfile, log_fp=sys.stderr).get_entries()
  except:
    import traceback; traceback.print_exc()
    sys.exit(1)

  try:
    # Optionally resolve cross-references
    if min_crossrefs is not None:
      db = biblib.bib.resolve_crossrefs(
        db, min_crossrefs=min_crossrefs)
  except biblib.messages.InputError:
    #sys.exit(1)
    pass


  ents = []
  for idx, ent in enumerate(db.values()):
    if not ent.key: continue
    if ent.typ.lower() in entry_types:
      keys = entry_keys
    else:
      ents.append(ent)
      continue


    vals = [" ".join(ent.get(key, '').split("\n")) for key in keys]
    # only keep keys that have non-null values
    fields = dict(filter(lambda p: p[1], zip(keys, vals)))
    fields = fix_synonyms(fields, synonyms)

    # change paper entries into @inproceedings
    newent = biblib.bib.Entry(fields.items())
    newent.typ = 'inproceedings'
    newent.key = ent.key
    ents.append(newent)

  return ents


def print_entries(printout, out, sort):
  """
  print entries to stdout, and optionally, if out is not None, write to file
  """

  q = """
  SELECT type, key, title, year, newbook as booktitle, author, howpublished, publisher, url
  FROM entries as E,
      (SELECT booktitle as oldbook, booktitle as newbook 
        FROM (SELECT distinct booktitle FROM entries) as foo 
        WHERE booktitle NOT IN (SELECT oldbook FROM mapping)
        UNION 
        select oldbook, newbook from mapping) as M
  WHERE E.booktitle = M.oldbook
  """

  if sort:
    if sort == 'booktitle':
      order = "ORDER BY newbook"
    else:
      order = "ORDER BY %s" % sort
    q += "\n" + order

  ents = sql_to_entries(q)

  # print to standard out
  if printout:
    for ent in ents:
      print(ent.to_bib())

  # log to file
  if out:
    with open(out, 'w') as f:
      for ent in ents:
        f.write(ent.to_bib())
        f.write('\n')

def save_entries(entries):
  """
  insert entries into database
  """
  for e in entries:
    keys = set(e.keys()).intersection(allowed_keys)
    vals = list(map(e.get, keys))
    args = (
        ", ".join(keys),
        ", ".join(["?"] * len(vals))
    )
    q = "INSERT INTO entries(key, type, %s) VALUES(?, ?, %s)" % args
    try:
      engine.execute(q, tuple([e.key, e.typ] + vals))
    except sqlalchemy.exc.IntegrityError:
      continue
    except Exception as err:
      print(e)





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
    booktitle=['booktile', 'journal', 'article', 'publisher']
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
      if syn in fields and fields[syn]:
        fields[key] = fields.get(syn)
        del fields[syn]
        break
  return fields


def tuple_to_entry(keys, row):
  # turn tuples into biblib.bib.Entry objects
  list(map(keys.remove, filter(lambda v: v in keys, ['type', 'key'])))
  d = dict([(key, str(row[key])) for key in keys if row[key]])
  ent = biblib.bib.Entry(d.items())
  ent.typ = row['type']
  ent.key = row['key']
  return ent

def sql_to_entries(q, args=()):
  print(" ".join(q.split("\n")))

  # turn tuples into biblib.bib.Entry objects
  ents = []
  cur = engine.execute(q, args)
  keys = cur.keys()
  list(map(keys.remove, ['type', 'key']))
  for row in cur:
    ents.append(tuple_to_entry(keys, row))
  return ents



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
from urllib import parse
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for

from .util import *

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
print(tmpl_dir)
app = Flask(__name__, template_folder=tmpl_dir)

DATABASEURI = "sqlite:///bibcleaner.db"
engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
  try:
    g.conn = engine.connect()
  except:
    traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  try:
    if hasattr(g, 'conn'):
      g.conn.close()
  except Exception as e:
    print(e)
    pass


@app.route('/upload/', methods=["POST", "GET"])
@app.route('/upload', methods=["POST", "GET"])
def upload():
  if 'bibtex' not in request.form:
    return render_template("upload.html")
  text = request.form['bibtex']
  fpath = tempfile.NamedTemporaryFile().name
  fname = os.path.basename(fpath)
  with open(fpath, 'w') as f:
    f.write(text)
    f.flush()
    with open(fpath, 'r') as rf:
      entries = load_bibfile(rf)

  cur = g.conn.execute("insert into files values(?)", (fname,))
  fid = cur.lastrowid
  save_entries(entries)
  q = """insert into file_entries 
  select %s, e.rowid
  from entries as e
  where e.key in (%s)"""
  args = (fid, ','.join(["'%s'" % e.key for e in entries]))
  g.conn.execute(q % args)
  return redirect(url_for("index", fname=fname))

@app.route("/files/") 
@app.route("/files")
def list_files():
  q = "select rowid, name from files"
  cur = g.conn.execute(q)
  ds = [dict(id=row[0], fname=row[1]) for row in cur]
  return render_template('list_files.html', files=ds)


@app.route("/print/<fname>") 
@app.route("/print/<fname>/") 
def print_file(fname=""):
  if fname.lower() in ['all', '']:
    q = """
    SELECT type, key, title, year, newbook as booktitle, author, howpublished, publisher, url
    FROM entries as E,
        (SELECT booktitle as oldbook, booktitle as newbook 
          FROM (SELECT distinct booktitle FROM entries) as foo 
          WHERE booktitle NOT IN (SELECT oldbook FROM mapping) or booktitle is null
          UNION 
          select oldbook, newbook from mapping) as M
    WHERE E.booktitle = M.oldbook or (E.booktitle is null and M.oldbook is null)
    """
    ents = sql_to_entries(q)
  else:
    q = """
    SELECT type, key, title, year, newbook as booktitle, author, howpublished, publisher, url
    FROM entries as E, files as f, file_entries as fe,
        (SELECT distinct booktitle as oldbook, booktitle as newbook 
          FROM (SELECT distinct booktitle FROM entries) as foo 
          WHERE (booktitle NOT IN (SELECT oldbook FROM mapping) or 
                 booktitle is null)
          UNION 
          select oldbook, newbook from mapping) as M
    WHERE (E.booktitle = M.oldbook or 
           (E.booktitle is null and M.oldbook is null)) and 
          fe.fid = f.rowid and 
          fe.eid = E.rowid and
          f.name = ?
    """
    ents = sql_to_entries(q, (fname,))
  bibtex = '\n'.join([e.to_bib() for e in ents])
  return render_template('print.html', bibtex=bibtex)


@app.route('/', methods=["POST", "GET"])
@app.route('/<fname>', methods=["POST", "GET"])
@app.route('/<fname>/', methods=["POST", "GET"])
def index(fname=""):
  if fname.lower() in ('all', ''):
    cur = g.conn.execute("""
      SELECT booktitle, count(*) 
      FROM entries
      WHERE booktitle is not null and
            booktitle NOT IN (SELECT oldbook FROM mapping UNION SELECT newbook FROM mapping) 
      GROUP BY booktitle 
      ORDER BY booktitle;""")
  else:
    cur = g.conn.execute("""
      SELECT booktitle, count(*) 
      FROM entries, file_entries as fe, files as f
      WHERE booktitle is not null and
            booktitle NOT IN (SELECT oldbook FROM mapping UNION SELECT newbook FROM mapping) AND
            f.rowid = fe.fid and
            entries.rowid = fe.eid and
            f.name = ?
      GROUP BY booktitle 
      ORDER BY booktitle;""", (fname,))

  books = [dict(name=row[0], count=row[1]) for row in cur]
  cur = g.conn.execute("SELECT oldbook, newbook, rowid FROM mapping")
  mapping = [dict(oldbook=row[0], newbook=row[1], id=row[2]) for row in cur]

  tmp = defaultdict(list)
  for d in mapping:
    tmp[d['newbook']].append(d)
  gmapping = []
  for item in tmp.items():
    gmapping.append(dict(newbook=item[0], oldbooks=item[1]))
  gmapping.sort(key=lambda d: d['newbook'])

  context = dict(books = books, mapping=mapping, gmapping=gmapping, fname=fname)
  return render_template("index.html", **context)


@app.route('/rm/', methods=['POST', 'GET'])
def rm_mapping():
  try:
    id = request.form['id']
    q = "DELETE FROM mapping WHERE rowid = ?"
    g.conn.execute(q, (id,))
    return json.dumps(dict(status="OK"))
  except Exception as ee:
    print(ee)
    return json.dumps(dict(status="ERR"))

@app.route('/set/', methods=['POST', 'GET'])
def new_mapping():
  try:
    print(request.form)

    old = parse.unquote(request.form['oldbook'])
    new = request.form['newbook']
    print((old, new))
    try:
      q = """INSERT INTO mapping(oldbook, newbook) VALUES(?, ?)"""
      cur = g.conn.execute(q, (old, new))
      rowid = cur.lastrowid
      if rowid is not None:
        return json.dumps(dict(status="OK", id=rowid))
    except Exception as e:
      return json.dumps(dict(status="ERR", msg=str(e)))
      print(e)
  except Exception as ee:
    print(ee)
    return json.dumps(dict(status="ERR"))

def run_server(HOST='localhost', PORT=8000, threaded=False, debug=True):
  print("Point your browser to: http://%s:%d" % (HOST, PORT))
  app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)



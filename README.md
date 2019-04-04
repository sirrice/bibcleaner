# Purpose

Papers have page limits.
Bibtex files are ridiculously messy, contain a ton of extraneous attributes that make the references ugly, inconsistent, and push you over the page limit.    Consider this example:

      @article{Kalashnikov06,
      author = {Kalashnikov, Dmitri V. and Mehrotra, Sharad},
      title = {Domain-independent Data Cleaning via Analysis of Entity-relationship Graph},
      journal = {ACM Transactions on Database Systems},
      issue_date = {June 2006},
      volume = {31},
      number = {2},
      month = jun,
      year = {2006},
      issn = {0362-5915},
      pages = {716--767},
      numpages = {52},
      doi = {10.1145/1138394.1138401},
      acmid = {1138401},
      publisher = {ACM},
      address = {New York, NY, USA},
      }

We only actually care about author, title, journal, and year.  The rest waste space.

There are also multiple entry types, each with their own format (I realize there are subtle differences that I choose to ignore):

* inproceedings
* journal
* article

Booktitles/journals have pretty much no standard.  Consider the following versions of "SIGMOD":

      Proceedings of the 2000 ACM SIGMOD International Conference on Management of Data
      Proceedings of the 2010 ACM SIGMOD International Conference on Management of Data
      Proceedings of the 2010 ACM SIGMOD International Conference on Management of data
      Proceedings of the 2012 ACM SIGMOD International Conference on Management of Data
      Proceedings of the 2013 ACM SIGMOD International Conference on Management of Data
      Proceedings of the 2014 ACM SIGMOD International Conference on Management of Data
      Proceedings of the 2014 ACM SIGMOD international conference on Management of data
      Proceedings of the 2015 ACM SIGMOD International Conference on Management of Data
      SIGMOD
      SIGMOD Conference
      Proceedings of the 2003 ACM SIGMOD international conference on Management of data
      Proceedings of the 2007 ACM SIGMOD international conference on Management of data
      Proceedings of the 1997 ACM SIGMOD International Conference on Management of Data
      In Proceedings of ACM SIGMOD

Why? WHY? 

## BibCleaner

bibcleaner is a utility  that:

* parses (using [biblib](https://github.com/aclements/biblib)) and loads a bibtex file and throws out
  the unnecessary entry attributes.  It keeps sane attributes for non-inproceedings/journa/article
  entries.
* the entries are saved in a sqlite database that can be queried
* runs a small webserver with a simple GUI to clean the booktitles in your entries
* once you've cleaned enough booktitles, export a clean, succinct version of your bibtex file,
  optionally sorted by year, author (lexigraphically), entry key, or booktitle.


# Interface

![Screenshot](https://raw.githubusercontent.com/sirrice/bibcleaner/master/screenshot.png)

The above is a screenshot of the `bibcleaner` interface.  The middle panel shows the list of unique booktitles in your bibtex file.  
Use the input box to type in a new value for the highlighted booktitle, or an empty string to accept the existing value.
Up and down arrow keys work and we try really hard to make the interface keyboard only, and efficient.

The left panel shows the mappings you have already created.  The blue text is the short normalized booktitle, and the red text are the original variations that map to the blue text.
Click on a red text to remove that mapping.

You can upload bibtex files, list the files you've uploaded, and export a clean bibtex file

# Installation and Usage

This library requires:

* **Python3**
* [biblib](https://github.com/sirrice/biblib)
* [flask](http://flask.pocoo.org/)
* [click](click.pocoo.org)
* sqlalchemy

Do the following

      # Setup a clean virtual env
      virtualenv new --python=<path to python3> <venv name>

      # Install custom biblib
      git clone https://github.com/sirrice/biblib.git
      cd biblib
      python setup.py install

      # Install bibcleaner
      pip install bibcleaner

## Running the GUI

The easiest is to just run the server and use the gui (click help in the upper right for instructions)

      ./bibcleaner --server --port 8000
      # go to localhost:8000


#### Command Line Usage

Help

      ./bibcleaner --help


Add entries

      ./bibcleaner --bibname <path to bib file>

Clean up an existing bibtex file and print to stdout

      ./bibcleaner --bibname <path> --printout

After normalizing the book titles, output the cleaned entries into a new file

     ./bibcleaner --out <path to output bibtex file> 

Or output them sorted by booktitle, author name or another attribute

    ./bibcleaner --out <path> --sort booktitle

Now you're under the page limit!


# Kudos

We're using aclement's [biblib](https://github.com/aclements/biblib) with a tiny hack to ignore parsing errors.

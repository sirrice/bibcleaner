# Purpose

Bibtex files are ridiculously messy, and the primary fields that matter are the authors, the 
paper title, the book title, and the year of publications.  Unfortunately there are 
_way too many_ formats for this!  

There are numerous extraneous attributes in a typical bibtex entry that have no right
to be in my paper!  Consider this example:


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

90% OF THESE ATTRIBUTES ARE TAKING UP PRECIOUS SPACE!  GO AWAY

There are also multiple entry types, each with their own format (I realize there are subtle differences):

* inproceedings
* journal
* article

Booktitles/journals have pretty much no standard.  Consider the following versions of "SIGMOD":

        Proceedings of the 2000 ACM SIGMOD International Conference on Management of Data
        Proceedings of the 2006 ACM SIGMOD International Conference on Management of Data
        Proceedings of the 2008 ACM SIGMOD International Conference on Management of Data
        Proceedings of the 2009 ACM SIGMOD International Conference on Management of Data
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

Why? WHY?   They are also excessively long and taking up my precious space.

## BibCleaner

bibcleaner is a utility  that performs the following

* parses (using [biblib](https://github.com/aclements/biblib)) loads a bibtex file and throws out
  the unnecessary entry attributes.  It's kind and keeps sane attributes for non-inproceedings/journa/article
  entries.
* the entries are saved in a sqlite database that can be queried
* runs a small webserver with a simple GUI to clean the booktitles in your entries
* once you've cleaned enough booktitles, export a clean, succinct version of your bibtex file,
  optionally sorted by year, author (lexigraphically), entry key, or booktitle.


# Installation and Usage

Requires

* Python3
* [biblib](https://github.com/aclements/biblib)
* [flask](http://flask.pocoo.org/)
* [click](click.pocoo.org)
* sqlalchemy


We recommend usin a virtualenv environment for all of the following

        git clone https://github.com/aclements/biblib.git
        cd biblib
        python3 setup.py install

        pip3 install flask sqlalchemy click 

Help: options can be combined

        ./bibcleaner --help

Add entries

        ./bibcleaner --bibname <path to bib file>

Clean up an existing bibtex file and print to stdout

        ./bibcleaner --bibname <path> --printout

Run server (click help in the upper right for instructions)

        ./bibcleaner --server
        # go to localhost:8000

After normalizing the book titles

       ./bibcleaner --out <path to output bibtex file> 

Or sorted

      ./bibcleaner --out <path> --sort booktitle

Now you're under the page limit!

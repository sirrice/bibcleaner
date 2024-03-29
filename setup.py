from distutils.core import setup

setup(
    name='bibcleaner',
    version='0.0.12',
    description='Super simple bibtex cleaner and normalizer',
    url='https://github.com/sirrice/bibcleaner',
    author='Eugene wu',
    author_email='ewu@cs.columbia.edu',
    packages=['bibcleaner', 'bibcleaner.templates', 'bibcleaner.static'],
    include_package_data=True,
    package_data={
      'bibcleaner':['static/*', 'templates/*']
    },
    scripts=['bin/bibcleaner'],
    keywords=['bibtex', 'tex', 'cleaning'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Database',
        'Topic :: Text Processing',
    ],
    long_description='see http://github.com/sirrice/bibcleaner',
    install_requires = [ 
        'click', 
        'sqlalchemy==1.4',
        'Flask', 
        'biblib @ git+ssh://git@github.com/sirrice/biblib.git'
        ],
    dependency_links=['https://github.com/sirrice/biblib/archive/master.zip']
)

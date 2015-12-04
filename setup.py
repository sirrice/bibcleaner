from distutils.core import setup

setup(
    name='bibcleaner',
    version='0.0.1',
    description='Poor man\'s bibtex cleaner and normalizer',
    url='https://github.com/sirrice/bibcleaner',
    author='Eugene wu',
    author_email='ewu@cs.columbia.edu',
    packages=['bibcleaner'],
    scripts=['bin/bibcleaner'],
    keywords=['bibtex', 'tex', 'cleaning'],
    classifiers=[
        'Development Status :: 0 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Database',
        'Topic :: Text Processing',
    ],
    long_description=open('README.md').read(),
    install_requires = [ 'click', 'sqlalchemy', 'flask' ],
    dependency_links=['https://github.com/sirrice/biblib/archive/master.zip']
)

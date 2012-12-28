# ckanext-dgutests

Provides simple selenium tests to be run against a CKAN instance that is also using the ckanext-dgu plugin.

## Install

    git clone git://github.com/rossjones/ckanext-dgutests.git
    cd ckanext-dgutests
    python setup.py develop

## Commands

To install selenium ready for use:

    paster runtests install

To run the tests

    paster runtests run

If you don't specify the host:port pair using -s then the paster command will start its
own version of selenium
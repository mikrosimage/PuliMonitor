PuliMonitor
==========

PuliMonitor is a user interface to interact with OpenRenderManagement. 
It is not ready for primetime yet, but actively worked on by Mikros Image 
and rise|fx. 

System requirements
-------------------

PuliMonitor is targeted to run on Linux and Windows, but "should" work on any platform the supports the following libraries:

Python 2.6/2.7 with following modules :

   * PyQt4
   * sip
   * requests
   * OpenRenderManagement


Installation
------------

1. Make sure the above packages can be found by Python.
2. Modify config/general.ini to find your server
3. From the PuliMonitor directory run main.py


Building the documenatation
---------------------------

1. install Python Sphinx
2. in the "docs" subfolder run:
```sh
make html
```

To automatically create docs from the source files:

```sh
cd docs/
sphinx-apidoc -f -o . ../src
```


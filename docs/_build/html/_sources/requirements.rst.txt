
Installation
============

.. _started:

Required packages
-----------------

Install the following packages on a debian-based distribution:

::

    sudo apt-get install mongodb-server ipython3


Start also the following system services:
      
::

    sudo service mongodb-server start


Developers
----------

.. First, install some :download:`[dependencies]<snippets/requirements.txt>`:

First, install some dependencies:

::

  pip3 install --upgrade pymongo pyqt5 PySide2

Install this package with (assuming $HOME/python3 is on your $PYTHONPATH):

::

  cd ~/python3_packages
  git clone https://github.com/elsampsa/cute_mongo_forms
  cd cute_mongo_forms
  ln -s $PWD/cute_mongo_forms $HOME/python3

.. _production:

Production users
----------------

Production users should use this command to install the latest version:

::

  pip3 install --upgrade git+git://github.com/elsampsa/cute_mongo_forms
  
.. some other possible commands:
.. pip3 install --upgrade git+ssh://user@[your-personal-git-repository]/cute_mongo_forms
  
  
.. note:: Pip installation pulls python binary packages that are available at the PyPi repository.  Installation has been tested on Ubuntu 16.04 LTS, x86_64 with Python 3.5.  Should work also on more recent linux versions / setups.
  
Test the package
----------------

Test your dependencies with:

::

  ipython3
  import pymongo
  import PyQt5
  import PySide2


Quicktest the example:

::

  ipython3
  from cute_mongo_forms.example import main
  main()



Installation
============

.. _started:

Required packages
-----------------

Install the following packages on a debian-based distribution:

::

    sudo apt-get install mongodb-server ipython3


If you are going to use mongodb with this library, start also the following system services:
      
::

    sudo service mongodb-server start

If that doesn't work, try this:

::

    sudo systemctl start mongodb.service


Install from PyPi with:


::

    pip3 install --user --upgrade cute_mongo_forms
    
    
Or from GitHub with:
    

::

  pip3 install --user --upgrade git+git://github.com/elsampsa/cute_mongo_forms
  
  
Test the package
----------------

Quicktest the example:

::

  ipython3
  from cute_mongo_forms.example import main
  main()


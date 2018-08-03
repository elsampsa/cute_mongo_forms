Now what?
---------

The column classes, widget layouts and Qt styles used in the tutorial are elementary and crude.  To make them look and feel more pro, you should implement your own.

If you want custom behaviour for the form fields, say, form fields that only accept integers, web addresses, etc. you should implement a custom "Column" class that uses a QValidator with an input mask.

When you implement custom columns and contribute them back to this library (remember, LGPL), they should be placed under the "column/" directory (i.e. in the column submodule) in a separate file (not into "base.py").  Same goes for Row, Container and Collection classes.

Don't forget to try the example provided with this library.  It demonstrates a much more complex case.

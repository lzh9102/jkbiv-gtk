JKB Image Viewer
================

This is a work in progress to create a small and handy image viewer based on
the `pygtk <http://www.pygtk.org/>`_ toolkit.

Usage
-----

::

   jkbiv [-h] [path]

Options
~~~~~~~

-h
   display help message

``path``
   the file or directory to open

Settings
--------

.. warning:: This program is a work in progress, so the options and the file
   format may change at any time.

The setting of *jkbiv* can be set in ``~/.jkbivrc``, a dotfile inside the
user's home directory. This program doesn't create the file; you have to create
it manually. The config file is in *ini* format; here's an example of a config
file:

.. code:: ini

   [keymap]
   quit = q
   next = l <right> <C-n> <space>
   prev = h <left> <C-p> <backspace>
   fullscreen = f

The text enclosed by square brackets ``[]`` is the beginning of a *section*.
Subsequent lines belong to the section until encountering a new section header.
Options are in the form ``<key> = <value>``.

Available sections and options are documented as follows.

*keymap* Section
~~~~~~~~~~~~~~~~

The *keymap* section contains the shortcut bindings options. The keys are the
function names, and the values are (zero, one or multiple) keys that are mapped
to the function. For example, ``quit = q <C-x><C-c>`` maps both the *q* key and
the *Ctrl-x* *Ctrl-c* key sequence to the ``quit`` function. Note that there
are no whitespace characters between ``<C-x>`` and ``<C-c>``. Here is a
list of available functions:

================== ===============
   function name     description
================== ===============
   quit              exit the program
------------------ ---------------
   next              next image
------------------ ---------------
   prev              previous image
------------------ ---------------
   fullscreen        toggle fullscreen mode
================== ===============

Todo
----

Here are several functions I want to implement:

- auto reload when file or directory changes
- zoom in/out
- load file in background
- preload and cache adjacent images

License
-------

Copyright (C) 2014 Che-Huai Lin <lzh9102@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

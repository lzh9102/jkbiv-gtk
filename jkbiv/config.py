from ConfigParser import SafeConfigParser, ParsingError
import codecs
import os
import StringIO

DEFAULT_CONFIG = """
[window]
fullscreen = false
width = 800
height = 600
[keymap]
quit = q <escape>
next = l j <right> <C-n> <space>
prev = h k <left> <C-p> <backspace>
fullscreen = f
zoom in = i zi + <C-=>
zoom out = o zo - <C-->
restore = zz = <C-0>
up = <C-k> <C-up>
down = <C-j> <C-down>
left = <C-h> <C-left>
right = <C-l> <C-right>
memory usage = m
"""

def loadConfig():
    config_file = os.path.join(os.path.expanduser("~"), ".jkbivrc")
    parser = SafeConfigParser()
    parser.readfp(StringIO.StringIO(DEFAULT_CONFIG))
    try:
        with codecs.open(config_file, 'r', encoding='utf-8') as f:
            parser.readfp(f)
    except IOError:
        print "warning: failed to read config file: %s" % config_file
    except ParsingError as e:
        print e
    return parser

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
quit = q
next = <right> <C-n> <space>
prev = <left> <C-p> <backspace>
fullscreen = f
zoom in = zi + <C-=>
zoom out = zo - <C-->
restore = zz = <C-0>
up = k
down = j
left = h
right = l
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

from ConfigParser import SafeConfigParser, ParsingError
import codecs
import os
import StringIO

DEFAULT_CONFIG = """
[keymap]
quit = q
next = l <right> <C-n> <space>
prev = h <left> <C-p> <backspace>
fullscreen = f
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

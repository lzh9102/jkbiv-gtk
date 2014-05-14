from baseapp import BaseApplication
from shortcut import ShortcutMapper, Keystroke, parseKeySequence
from res import DirectoryWalker
import sys
import resource
import config

class Application(BaseApplication):

    def __init__(self, width, height, url):
        super(Application, self).__init__(width, height)
        self.config = config.loadConfig()
        self.keymap = ShortcutMapper()
        self.setupKeymaps()
        self.dirwalker = DirectoryWalker(url)
        self.loadCurrentResource()

    def setupKeymaps(self):
        keymap = self.keymap
        config = self.config
        functions = {
            "quit": self.quit,
            "next": self.fnNext,
            "prev": self.fnPrev,
            "fullscreen": self.toggleFullscreen,
            "memory usage": self.fnPrintMemUsage,
        }
        # keybindings are written in the 'keymap' section
        for (name, value) in config.items('keymap'):
            if name in functions:
                # value is a space-delimited list of keybindings
                for keys in value.split():
                    keystrokes = parseKeySequence(keys)
                    if keys:
                        keymap.bind(keystrokes, functions[name])
                    else:
                        print "error: invalid keybinding value '%s'" % keys
            else:
                print "warning: unknown keybinding name '%s'" % name

    def onKeyPress(self, keystr):
        self.keymap.pressKey(Keystroke(keystr))

    def loadCurrentResource(self):
        res = self.dirwalker.currentResource()
        if res:
            self.loadImage(res.getUrl())
            self.redraw()

    def onDraw(self):
        res = self.dirwalker.currentResource()
        if res:
            self.drawText(res.getName(), 0, 0)
            self.setWindowTitle("jkbiv - %s" % res.getName())
        else:
            self.drawText("No Image", 0, 0)
            self.setWindowTitle("jkbiv")

    # user-reachable functions

    def fnNext(self):
        if self.dirwalker.next():
            self.loadCurrentResource()

    def fnPrev(self):
        if self.dirwalker.prev():
            self.loadCurrentResource()

    def fnPrintMemUsage(self):
        usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print "usage: %d" % usage

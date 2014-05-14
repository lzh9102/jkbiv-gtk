from baseapp import BaseApplication
from shortcut import ShortcutMapper, Keystroke
from res import DirectoryWalker
import sys
import os
import resource

class Application(BaseApplication):

    def __init__(self, width, height):
        super(Application, self).__init__(width, height)
        self.keymap = ShortcutMapper()
        self.setupKeymaps()
        if len(sys.argv) >= 2:
            directory = sys.argv[1]
        else:
            directory = os.getcwd()
        self.dirwalker = DirectoryWalker(directory)
        self.loadCurrentResource()

    def setupKeymaps(self):
        keymap = self.keymap
        # function to convert a string to Keystroke() list
        KSL = lambda keys: [Keystroke(key) for key in keys.split(" ")]
        # setup keymaps
        keymap.bind(KSL("q"), self.quit)
        keymap.bind(KSL("l"), self.fnNext)
        keymap.bind(KSL("right"), self.fnNext)
        keymap.bind(KSL("h"), self.fnPrev)
        keymap.bind(KSL("left"), self.fnPrev)
        keymap.bind(KSL("m"), self.fnPrintMemUsage)
        keymap.bind(KSL("f"), self.toggleFullscreen)

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

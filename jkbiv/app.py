from baseapp import BaseApplication
from shortcut import ShortcutMapper, Keystroke

class Application(BaseApplication):

    def __init__(self, width, height):
        super(Application, self).__init__(width, height)
        self.keymap = ShortcutMapper()
        self.setupKeymaps()

    def setupKeymaps(self):
        keymap = self.keymap
        # function to convert a string to Keystroke() list
        KSL = lambda keys: [Keystroke(key) for key in keys]
        # setup keymaps
        keymap.bind(KSL("q"), self.quit)

    def onKeyPress(self, keystr):
        self.keymap.pressKey(Keystroke(keystr))

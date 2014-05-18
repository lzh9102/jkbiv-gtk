import gtk
from displaywidget import DisplayWidget

def computeDrawingArea(windowWidth, windowHeight, imageWidth, imageHeight):
    """ Determine how to draw the image at the center of the window as large as
        possible and without cropping. Returns (x, y, width, height) of the
        computed area.
    """
    if windowWidth * imageHeight > windowHeight * imageWidth:
        # ih/iw > wh/ww: image size bounded by height
        width = imageWidth * windowHeight / imageHeight
        height = windowHeight
        x = (windowWidth - width) / 2
        y = 0
    else:
        # ih/iw <= wh/ww: image size bounded by width
        width = windowWidth
        height = imageHeight * windowWidth / imageWidth
        x = 0
        y = (windowHeight - height) / 2
    return (x, y, width, height)

# map gtk keyval name to key representation
KEYVAL_NAME_REPR = {
    'grave': '`',
    'asciitilde': '~',
    'exclam': '!',
    'at': '@',
    'numbersign': '#',
    'dollar': '$',
    'percent': '%',
    'asciicircum': '^',
    'ampersand': '&',
    'asterisk': '*',
    'parenleft': '(',
    'parenright': ')',
    'minus': '-',
    'underscore': '_',
    'equal': '=',
    'plus': '+',
    'braceleft': '{',
    'braceright': '}',
    'bracketleft': '[',
    'bracketright': ']',
    'backslash': '\\\\',
    'bar': '|',
    'semicolon': ';',
    'colon': ':',
    'apostrophe': "'",
    'quotedbl': '"',
    'comma': ',',
    'less': '\\<',
    'period': '.',
    'greater': '\\>',
    'slash': '/',
    'question': '?',
}

class BaseApplication(object):

    def __init__(self):
        window = gtk.Window()
        window.connect("destroy", gtk.main_quit)
        window.set_position(gtk.WIN_POS_CENTER)
        self.window = window

        # image display widget
        display = DisplayWidget()
        window.add(display)
        self.display = display

        self.is_fullscreen = False

        # events
        window.connect("key_press_event", self.__handleKeyPress)

        window.show_all()

    def run(self):
        gtk.main()

    def __isModifier(self, keystr):
        # TODO: improve efficiency by using numeric value
        return keystr.startswith("control_") or keystr.startswith("shift_") \
                or keystr.startswith("meta_") or keystr.startswith("alt_")

    def __handleKeyPress(self, widget, event):
        keystr = gtk.gdk.keyval_name(event.keyval).lower() # key name
        is_symbol = False
        if keystr in KEYVAL_NAME_REPR: # convert keystr to symbol
            keystr = KEYVAL_NAME_REPR[keystr]
            is_symbol = True
        if self.__isModifier(keystr): # ignore modifier keys
            return
        if event.state & gtk.gdk.SHIFT_MASK: # with shift key
            if not is_symbol: # don't prefix S- to symbols
                keystr = "S-" + keystr
        if event.state & gtk.gdk.CONTROL_MASK: # with control key
            keystr = "C-" + keystr
        if event.state & gtk.gdk.MOD1_MASK: # with alt (meta) key
            keystr = "A-" + keystr
        self.onKeyPress(keystr)

    def quit(self):
        self.window.destroy()

    def gtkExposeEvent(self, widget, event):
        (x, y, width, height) = event.area
        self.width = width
        self.height = height
        self.redraw()

    def loadImage(self, url):
        # TODO: implement image loader
        pixbuf = gtk.gdk.pixbuf_new_from_file(url)
        self.display.setPixbuf(pixbuf)

    def setWindowTitle(self, title):
        self.window.set_title(title)

    def setWindowSize(self, width, height):
        self.window.resize(width, height)

    def setFullscreen(self, fullscreen=True):
        if fullscreen:
            self.window.fullscreen()
        else:
            self.window.unfullscreen()
        self.is_fullscreen = fullscreen

    def toggleFullscreen(self):
        self.setFullscreen(not self.is_fullscreen)

    def zoomIn(self):
        self.display.zoom(+0.1)

    def zoomOut(self):
        self.display.zoom(-0.1)

    def moveViewPort(self, dx, dy):
        # moving viewport is the opposite direction of moving image
        self.display.moveImage(-dx, -dy)

    def restore(self):
        self.display.setZoomLevel(1.0)
        self.display.setOffset(0, 0)

    # event callbacks

    def onKeyPress(self, keystr):
        """ this function will be called when a key is pressed """
        pass

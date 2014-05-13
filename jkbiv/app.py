from baseapp import BaseApplication
import gtk

class Application(BaseApplication):

    def onKeyPress(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        print keyname

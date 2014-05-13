import gtk

class BaseApplication(object):

    def __init__(self, width, height):
        window = gtk.Window()
        window.connect("destroy", gtk.main_quit)
        window.set_size_request(width, height)
        window.set_position(gtk.WIN_POS_CENTER)
        self.window = window

        # drawing area
        drawarea = gtk.DrawingArea()
        drawarea.set_size_request(width, height)
        window.add(drawarea)
        #drawarea.window.set_background(gtk.gdk.Color(0, 255, 0))
        #drawarea.window.draw_text(self.gc, "hello")
        self.drawarea = drawarea

        self.width = width
        self.height = height

        # events
        window.connect("key_press_event", self.onKeyPress)

        window.show_all()

    # event callbacks

    def onKeyPress(self, widget, event):
        """ this function will be called when a key is pressed """
        pass

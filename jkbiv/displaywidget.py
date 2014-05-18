import gtk
import gobject
from gtk import gdk

class Rectangle(object):

    def __init__(self, x, y, width, height):
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and \
            self.width == other.width and self.height == other.height

    def __repr__(self):
        return "Rectangle(%d, %d, %d, %d)" % \
            (self.x, self.y, self.width, self.height)

    def left(self):
        return self.x

    def right(self):
        return self.x + self.width

    def top(self):
        return self.y

    def bottom(self):
        return self.y + self.height

    def computeScaledRect(self, scale, cx, cy):
        """ Return a new rectangle scaled with respect to (cx, cy) """
        assert(type(scale) == float)
        assert(type(cx) == int and type(cy) == int)
        (x0, y0, w0, h0) = (self.x, self.y, self.width, self.height)
        w1 = int(self.width * scale)
        h1 = int(self.height * scale)
        x1 = cx - int((cx - x0) * scale)
        y1 = cy - int((cy - y0) * scale)
        return Rectangle(x1, y1, w1, h1)

class DisplayWidget(gtk.Widget):
    """ A image-displaying widget """

    def __init__(self):
        gtk.Widget.__init__(self)

    def getZoomLevel(self):
        return self.zoomLevel

    def setZoomLevel(self, zoom):
        assert(type(zoom) == float)
        # resize the image area with respect to center of the window
        oldrect = self.computeImageRect()
        oldzoom = self.zoomLevel
        zoomRatio = zoom / oldzoom
        (cx, cy) = (self.getWidth() / 2, self.getHeight() / 2)
        newrect = oldrect.computeScaledRect(zoomRatio, cx, cy)
        # update the zoom level and position
        self.zoomLevel = zoom
        self.offsetX += newrect.x - oldrect.x
        self.offsetY += newrect.y - oldrect.y
        self.invalidateView()

    def zoom(self, diff):
        zoom = self.getZoomLevel() + diff
        if zoom < 0.1:
            zoom = 0.1
        elif zoom > 10:
            zoom = 10
        self.setZoomLevel(zoom)

    def getOffset(self):
        return (self.offsetX, self.offsetY)

    def setOffset(self, x, y):
        self.offsetX = x
        self.offsetY = y
        self.invalidateView()

    def moveImage(self, dx, dy):
        (x, y) = self.getOffset()
        r = self.computeImageRect()
        if (dx > 0 and r.left() < 0) or \
                (dx < 0 and r.right() > self.getWidth()):
            x += dx
        if (dy > 0 and r.top() < 0) or \
                (dy < 0 and r.bottom() > self.getHeight()):
            y += dy
        self.setOffset(x, y)

    def computeDefaultDrawingArea(self):
        """ Determine the appropriate size to display the image.
            If the image fits in the window, then display the original size.
            Otherwise, scale the image to the maximum size that fits in the
            window. """
        if not self.pixbuf: # no image allocated
            return None
        windowWidth = self.getWidth()
        windowHeight = self.getHeight()
        imageWidth = self.getImageWidth()
        imageHeight = self.getImageHeight()
        if imageWidth <= windowWidth and imageHeight <= windowHeight:
            # the original image fit in the window, no need to zoom
            x = (windowWidth - imageWidth) / 2
            y = (windowHeight - imageHeight) / 2
            return Rectangle(x, y, imageWidth, imageHeight)
        elif windowWidth * imageHeight > windowHeight * imageWidth:
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
        return Rectangle(x, y, width, height)

    def computeImageRect(self):
        """ Compute the boundaries of the image after zooming and translation.
        """
        rect = self.computeDefaultDrawingArea()
        # zooming and offset
        x = rect.x + self.offsetX
        y = rect.y + self.offsetY
        width = int(rect.width * self.zoomLevel)
        height = int(rect.height * self.zoomLevel)
        return Rectangle(x, y, width, height)

    def resetZoomAndOffset(self):
        self.zoomLevel = 1.0
        self.offsetX = self.offsetY = 0
        self.invalidateView()

    # events

    def do_realize(self):
        # set the widget to realized
        self.set_flags(self.flags() | gtk.REALIZED)
        # initialize window (drawing area)
        self.window = gdk.Window(
            self.get_parent_window(),
            width=self.allocation.width,
            height=self.allocation.height,
            window_type=gdk.WINDOW_CHILD,
            wclass=gdk.INPUT_OUTPUT,
            event_mask=self.get_events() | gdk.KEY_PRESS_MASK \
                | gdk.EXPOSURE_MASK)
        # associate the window (drawing area) with the widget itself
        self.window.set_user_data(self)
        # attach the style of self to the window
        self.style.attach(self.window)
        # set widget to parent window style
        self.style.set_background(self.window, gtk.STATE_NORMAL)
        self.window.move_resize(*self.allocation)
        # graphics context
        self.gc = self.style.fg_gc[gtk.STATE_NORMAL]
        # image pixbuf
        self.pixbuf = None
        # initialize zoom and offset variables
        self.resetZoomAndOffset()

    def do_unrealize(self):
        self.window.destroy()

    def do_expose_event(self, event):
        """ draw the widget """
        self.redraw()

    # width and height
    def getWidth(self):
        return self.allocation.width

    def getHeight(self):
        return self.allocation.height

    def getImageWidth(self):
        return self.pixbuf.get_width()

    def getImageHeight(self):
        return self.pixbuf.get_height()

    # drawing functions

    def redraw(self):
        self.redrawBackground()
        self.redrawImage()

    def redrawBackground(self):
        color = gtk.gdk.color_parse('#000')
        self.gc.set_rgb_fg_color(color)
        self.window.draw_rectangle(self.gc, True, 0, 0,
                                   self.getWidth(),
                                   self.getHeight())

    def redrawImage(self):
        if self.pixbuf:
            # compute image area
            rect = self.computeImageRect()
            # scale image
            new_pixbuf = self.pixbuf.scale_simple(rect.width, rect.height,
                                                  gtk.gdk.INTERP_BILINEAR)
            # draw image
            self.window.draw_pixbuf(self.gc, new_pixbuf, 0, 0, rect.x, rect.y)

    def invalidateView(self):
        self.window.invalidate_rect(self.allocation, True) # redraw widget

    # public methods

    def setPixbuf(self, pixbuf):
        self.pixbuf = pixbuf
        self.resetZoomAndOffset()
        self.invalidateView()

# register custom widget as a GObject
gobject.type_register(DisplayWidget)

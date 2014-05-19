# Load images from various sources to a pixbuf object
# All functions/class here must be reentrant

import gtk

def loadImageFromFile(path):
    """ Returns the pixbuf containing the loaded image. Returns None if failed.
    """
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file(path)
    except:
        return None
    return pixbuf

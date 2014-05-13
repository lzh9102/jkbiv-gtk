import gtk
from app import Application

def main():
    app = Application(width=800, height=600)
    gtk.main()
    Application().mainloop()

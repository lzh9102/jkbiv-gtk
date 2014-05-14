import gtk
import cProfile
from app import Application

def run():
    app = Application(width=800, height=600)
    gtk.main()

def main():
    profile = False
    if profile:
        profiler = cProfile.Profile()
        profiler.runcall(run)
        profiler.print_stats(sort=1)
    else:
        run()

import gtk
import cProfile
import argparse
from app import Application

def parse_args():
    parser = argparse.ArgumentParser(
        description="A keyboard-oriented image viewer")
    parser.add_argument("path", type=str, nargs='?', default="",
                        help="the file or directory to open")
    return parser.parse_args()

def run():
    args = parse_args()
    app = Application(800, 600, args.path)
    gtk.main()

def main():
    profile = False
    if profile:
        profiler = cProfile.Profile()
        profiler.runcall(run)
        profiler.print_stats(sort=1)
    else:
        run()

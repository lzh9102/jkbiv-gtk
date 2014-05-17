import cProfile
import argparse
from app import Application

def parse_args():
    parser = argparse.ArgumentParser(
        description="A keyboard-oriented image viewer")
    parser.add_argument("path", type=str, nargs='?', default="",
                        help="the file or directory to open")
    parser.add_argument("--profile", action="store_true", default=False,
                        help="the file or directory to open")
    return parser.parse_args()

def run(args):
    app = Application(args.path)
    app.run()

def main():
    args = parse_args()
    if args.profile:
        profiler = cProfile.Profile()
        profiler.runcall(run, args)
        profiler.print_stats(sort=1)
    else:
        run(args)

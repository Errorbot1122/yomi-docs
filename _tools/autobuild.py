from pathlib import Path
from subprocess import Popen
import sys

from watchdog.observers import Observer
import watchdog.events as wde

from make_rst import Repo_Directory, Template_Directory, parse_args, build_dir

LOG_PREFIX = "[yomi-autobuild] "

Python_Exec = Path(sys.executable).absolute()

Build_Directory = Repo_Directory / "_build"


# TODO: Fix ignore list
ignore_list = [
    "_tools",
    "_build",
    ".gitignore",
    "LICENSE",
    ".python-version",
]


def print_args(args: list) -> str:
    return " ".join([repr(x) if isinstance(x, str) else str(x) for x in args])


if __name__ == "__main__":
    Build_Directory.mkdir(exist_ok=True)
    source_dir = parse_args(sys.argv)["source_dir"]

    class SourceEventHandler(wde.FileSystemEventHandler):
        def on_any_event(self, event):
            event_types = [
                wde.FileSystemMovedEvent,
                wde.FileModifiedEvent,
                wde.FileCreatedEvent,
            ]

            correct_type = False
            for event_check in event_types:
                if isinstance(event, event_check):
                    correct_type = True
                    break

            if (
                correct_type
                and not event.is_directory
                and event.src_path.endswith("toml")
            ):
                print(
                    LOG_PREFIX
                    + f"Detected '{event.__class__.__name__}' in"
                    f" {source_dir.relative_to(Repo_Directory, walk_up=True)}!"
                    " Rebuilding..."
                )

                build_dir(source_dir)

    observer = Observer()
    event_handler = SourceEventHandler()

    observer.schedule(event_handler, path=Template_Directory)
    observer.schedule(event_handler, path=source_dir)

    process = None
    try:
        print(LOG_PREFIX + "Running initial build...")

        build_dir(source_dir)

        print(
            LOG_PREFIX
            + "Starting directory observer focused on"
            f" '{source_dir.relative_to(Repo_Directory, walk_up=True)}'"
        )
        observer.start()

        sphinx_args = [
            Python_Exec,
            "-m",
            "sphinx_autobuild",
            Repo_Directory,
            Build_Directory,
            "--ignore",
            ",".join({str(Repo_Directory / x) for x in ignore_list}),
        ]

        print(LOG_PREFIX + f"Starting command: `{print_args(sphinx_args)}`")
        process = Popen(
            sphinx_args,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        process.communicate()
        process.wait()

    except KeyboardInterrupt:
        print(f"\n{LOG_PREFIX}Interrupted by user. Shutting down gracefully...")
    except Exception as e:
        print(f"\n{LOG_PREFIX}Encountered unexpected error: {e}")
        raise e
    finally:
        print(LOG_PREFIX + "Stopping file observer...")
        observer.stop()
        observer.join()

        if process and process.poll() is None:
            print(LOG_PREFIX + "Terminating background sphinx process...")
            process.terminate()
            process.wait()

        print(LOG_PREFIX + "Shutdown complete.")
        sys.exit(0)

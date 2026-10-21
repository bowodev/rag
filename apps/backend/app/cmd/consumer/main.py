import argparse
import asyncio

from app.cmd.consumer.registry import CONSUMERS, get_consumer
from app.cmd.consumer.runner import run_consumer, run_many


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="DMT-RAG backend consumers")
    parser.add_argument("names", nargs="*", help="consumer name(s)")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--list", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.list:
        for name, spec in sorted(CONSUMERS.items()):
            print(f"{name:20} queue={spec.queue_name} model={spec.model.__name__}")
        return

    if args.all:
        specs = list(CONSUMERS.values())
    elif args.names:
        specs = [get_consumer(name) for name in args.names]
    else:
        raise SystemExit("pass consumer name(s) or --all. try --list")

    if len(specs) == 1:
        asyncio.run(run_consumer(specs[0]))
    else:
        asyncio.run(run_many(specs))


if __name__ == "__main__":
    main()
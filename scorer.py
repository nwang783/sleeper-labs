import argparse
import json
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--task", required=True, choices=["retrieve", "update", "export"])
    args = parser.parse_args()
    root = Path(args.workspace).resolve()
    sys.path.insert(0, str(root))
    sys.path.insert(0, "/benchmark")
    from probes.records_probe import run
    result = run(str(root), args.task)
    print(json.dumps(result))


if __name__ == "__main__":
    main()

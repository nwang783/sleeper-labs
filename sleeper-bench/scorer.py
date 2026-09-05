import argparse
import json
import time
import httpx


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--task", required=True, choices=["retrieve", "update", "export"])
    parser.add_argument("--suite", choices=["smoke", "rich"], default="smoke")
    args = parser.parse_args()
    from probes.records_probe import run
    # Readiness is separate from the probe: never retry a partially executed update.
    deadline = time.monotonic() + 20
    try:
        with httpx.Client(timeout=1, trust_env=False) as client:
            while True:
                try:
                    client.get(args.base_url + "/")
                    break
                except httpx.TransportError:
                    if time.monotonic() >= deadline:
                        raise
                    time.sleep(0.25)
        if args.suite == "rich":
            from probes.rich_probe import run as run_rich
            with httpx.Client(base_url=args.base_url, timeout=5, trust_env=False) as client:
                result = run_rich(client, args.task, "/state/records.sqlite")
        else:
            result = run(args.base_url, args.task)
    except (httpx.HTTPError, ValueError, AttributeError) as error:
        result = {"functional": False, "security": "broken",
                  "details": {"error": type(error).__name__}}
    print(json.dumps(result))


if __name__ == "__main__":
    main()

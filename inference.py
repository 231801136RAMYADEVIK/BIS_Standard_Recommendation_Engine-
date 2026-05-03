import json
import argparse
import traceback
import sys
sys.path.insert(0, ".")

from src.pipeline import get_recommendations


def main(input_path: str, output_path: str):
    with open(input_path, "r") as f:
        data = json.load(f)

    results = []
    for item in data:
        qid = item["id"]
        query = item["query"]
        try:
            standards, latency = get_recommendations(query)
        except Exception as e:
            print(f"[ERROR] id={qid}: {e}")
            traceback.print_exc()
            standards, latency = [], 0.0

        results.append({
            "id": qid,
            "expected_standards": item.get("expected_standards", []),
            "retrieved_standards": standards,
            "latency_seconds": latency
        })
        print(f"[OK] id={qid} | {standards} | {latency}s")

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nDone. {len(results)} results → {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    main(args.input, args.output)
import os, json

def main():
    dirp = os.path.join(os.getcwd(), "artifacts", "heals")
    events_path = os.path.join(dirp, "events.jsonl")
    if not os.path.exists(events_path):
        print("No heal events found.")
        return
    with open(events_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    events = [json.loads(l) for l in lines]
    rows = [
        f"| {e['elementId']} | {e['oldPrimary']['type']}: {e['oldPrimary']['value']} | "
        f"{e['healedWith']['type']}: {e['healedWith']['value']} | {e['score']:.2f} | {e['pageUrl']} | {e['timestamp']} |"
        for e in events
    ]
    md = "\n".join([
        "# Self-Healing Summary",
        "",
        "| Element ID | Old Primary | Healed With | Score | URL | Time |",
        "|---|---|---|---:|---|---|",
        *rows,
        ""
    ])
    os.makedirs(dirp, exist_ok=True)
    with open(os.path.join(dirp, "summary.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print("Wrote artifacts/heals/summary.md")

if __name__ == "__main__":
    main()

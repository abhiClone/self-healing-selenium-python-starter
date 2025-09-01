import json
import os


def main():
    heals_dir = os.path.join(os.getcwd(), 'artifacts', 'heals')
    events_path = os.path.join(heals_dir, 'events.jsonl')
    if not os.path.exists(events_path):
        print("No heal events found.")
        return
    summary = []
    with open(events_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                event = json.loads(line.strip())
                summary.append(event)
            except json.JSONDecodeError:
                continue
    if not summary:
        print("No heal events found.")
        return
    # Write summary.md
    md_path = os.path.join(heals_dir, 'summary.md')
    with open(md_path, 'w', encoding='utf-8') as md:
        md.write("| Element ID | Updated Strategies |\n")
        md.write("|------------|------------------|\n")
        for event in summary:
            element_id = event.get('id')
            updated = event.get('updated', {})
            strategies = updated.get('strategies', [])
            strat_desc = ', '.join([f"{s['type']}={s['value']}" for s in strategies])
            md.write(f"| {element_id} | {strat_desc} |\n")
    print(f"Heal summary written to {md_path}")


if __name__ == '__main__':
    main()
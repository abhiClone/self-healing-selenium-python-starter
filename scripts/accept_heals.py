import os, json, glob

def main():
    reg_path = os.path.join("config", "locators.json")
    heals_dir = os.path.join("artifacts", "heals")
    if not os.path.exists(heals_dir):
        print("No heals directory found.")
        return
    patches = glob.glob(os.path.join(heals_dir, "*.patch.json"))
    if not patches:
        print("No patch files to apply.")
        return
    with open(reg_path, "r", encoding="utf-8") as f:
        reg = json.load(f)
    for p in patches:
        with open(p, "r", encoding="utf-8") as f:
            patch = json.load(f)
        reg[patch["id"]] = patch["updated"]
        print("Applied patch:", os.path.basename(p))
    with open(reg_path, "w", encoding="utf-8") as f:
        json.dump(reg, f, indent=2)
    print("Updated config/locators.json")

if __name__ == "__main__":
    main()

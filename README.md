# Self-Healing Selenium (Python + Pytest)

A production-style **self-healing** test automation starter using **Selenium 4 + Python + Pytest**:
- Fallback strategies (CSS / XPATH / TEXT) with weights
- Similarity scoring using DOM attributes
- Heal events -> `artifacts/heals/events.jsonl`
- Patch proposals -> `artifacts/heals/*.patch.json`
- Embedded Flask demo server (no external app needed)

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest
```

The tests will:
1) Start a demo server at `http://localhost:3000`
2) Run a normal login test
3) Run a **broken** variant that changes the DOM
4) Still pass due to **self-healing**
5) Write artifacts to `artifacts/heals/` and a patch proposal

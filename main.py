"""
Entry point for Doctor vs Vaidya Prescription Comparator.
Can be executed directly with:
  python main.py
or
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""

import uvicorn
from app.main import app

def main():
    print("Starting Doctor vs Vaidya (Prescription Comparator) server on http://localhost:8000 ...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()

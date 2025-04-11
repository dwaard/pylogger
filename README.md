# PyLogger
a Project intended to grow into the swiss armyknife of real-time dataloggers.

# Usage
## Step 0: Setup
1. Create a `.env` file using the `.env.example`. 
1. Install Python and pip
1. Install Venv `pip install virtualenv`
1. Initialize Venv: `python -m venv .venv`
1. Activate venv using 
  - Windows: `.venv\Scripts\activate`
  - Windows (powershell): 
    1. `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force`
    1. `.venv\Scripts\activate.ps1`
  - Linux: `source .venv/bin/activate`
1. When activated, you can install dependencies using `pip`:
  - For instance using the `requirements.txt` file: `pip install -r requirements.txt`
  - Or simply: `pip install <package-name>` (do NOT install globally)

## Step 1: run the app
When you use venv:
1. Run the app: `python main.py`
1. Deactivate when you're done: `deactivate` (Windows and Linux)


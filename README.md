# Credit Rating Calculator for Residential Mortgage-Backed Securities (RMBS)

## Overview
This project implements a credit rating calculation system for Residential Mortgage-Backed Securities (RMBS) based on specific risk assessment criteria.

## Project Structure

```
├── credit_rating.py        # Main application file containing the credit rating logic and risk strategies
├── pyproject.toml          # Configuration file for project dependencies and build system
├── README.md               # README Doc
├── rmbs.json               # Example JSON file containing sample mortgage data for testing
├── test_credit_rating.py  # Test suite for validating the functionality of the credit rating system
└── uv.lock                 # Lock file for the `uv` virtual environment manager
```


## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- `uv` (Universal Virtual Environment Manager)

### Steps to Set Up the Project
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd crisil_assignment
   ```

2. Create virtual env
    ```
    uv venv
    ```

3. Activate Virtual env
    ```bash
    source .venv/bin/activate # For Mac and Linux only
    ```

3. Install dependencies
    ```bash
    uv sync
    ```
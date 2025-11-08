#!/bin/bash
set -e

echo "Checking for Python 3.12..."
if ! command -v python3.12 &> /dev/null

echo "Creating virtual environment (venv) with Python 3.12..."
python3.12 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip, setuptools and wheel..."
pip install --upgrade pip setuptools wheel

echo "Installing dependencies (Streamlit, Pandas, NumPy, PuLP)..."
pip install streamlit pandas numpy pulp

echo "Setup complete."
echo "To activate later, run: source venv/bin/activate"

#!/bin/bash
# Check if env exists, if not tell user
if [ ! -d "env" ]; then
    echo "Virtual environment not found. Please run 'python3 -m venv env' and 'source env/bin/activate' then 'pip install -r requirements.txt' first."
    exit 1
fi

# Run the bot using the virtual environment python
./env/bin/python main.py

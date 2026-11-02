#!/usr/bin/env bash
set -e
python3 score.py
python3 build_workbooks.py
python3 build_report.py

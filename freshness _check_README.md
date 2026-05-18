Dashboard Data Freshness Fix

PROBLEM
Dashboard query returned empty results after 3 months. No errors in logs.

ROOT CAUSE
DB was UTC, data was IST. New source backfilled 5.5 hours ahead.
WHERE date >= CURRENT_DATE - 7 missed recent data.

FIX
- Normalized all timestamps to UTC with AT TIME ZONE
- Added 30% row count drop alert
- Added per-source logging

HOW TO RUN
1. pip install -r requirements.txt
2. cp.env.example.env and fill credentials
3. python freshness_check.py
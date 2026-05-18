# Dashboard Freshness Monitor

Lightweight Python script that detects stale data and timezone mismatches in Postgres-backed dashboards.

## Problem
Dashboard queries started returning empty results after 3 months. No errors in logs. 
Root cause: Database stored UTC, but new data source backfilled in IST. 
`WHERE date >= CURRENT_DATE - 7` missed records 5.5 hours ahead.

## Solution
Script normalizes all timestamps to UTC, checks row counts per source, and alerts if any source drops 30%+ week-over-week.
Logs latest timestamps for quick debugging.

## Features
- UTC/IST timezone normalization using SQLAlchemy
- Row count comparison vs previous week
- Configurable alert threshold
- Runs in <10s on 1M+ row tables

## Tech Stack
Python 3.9+, Pandas, SQLAlchemy, python-dotenv

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your Postgres connection string
4. Run: `python freshness_check.py`

## Why This Matters
Shows ability to debug silent failures, understand timezone issues in distributed systems, 
and implement proactive monitoring that prevents bad data from reaching stakeholders.

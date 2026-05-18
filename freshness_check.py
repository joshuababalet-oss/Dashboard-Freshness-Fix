import os
import pandas as pd
from sqlalchemy import create_engine, text
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(filename='freshness_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

DB_CONN = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

def check_row_counts(engine):
    query = text("""
        SELECT
            source,
            COUNT(*) as row_count,
            MAX(order_date AT TIME ZONE 'UTC') as latest_ts
        FROM orders
        WHERE order_date AT TIME ZONE 'UTC' >= NOW() AT TIME ZONE 'UTC' - INTERVAL '7 days'
        GROUP BY source
    """)
    df = pd.read_sql(query, engine)
    logging.info(f"Current row counts:\n{df}")

    for _, row in df.iterrows():
        source = row['source']
        current_count = row['row_count']
        hist_query = text(f"""
            SELECT COUNT(*) FROM orders
            WHERE source = '{source}'
            AND order_date AT TIME ZONE 'UTC' BETWEEN
                NOW() AT TIME ZONE 'UTC' - INTERVAL '14 days'
                AND NOW() AT TIME ZONE 'UTC' - INTERVAL '7 days'
        """)
        prev_count = pd.read_sql(hist_query, engine).iloc[0, 0]
        if prev_count > 0:
            drop_pct = (prev_count - current_count) / prev_count
            if drop_pct > 0.3:
                alert_msg = f"ALERT: {source} dropped {drop_pct:.0%} week-over-week"
                logging.warning(alert_msg)
                print(alert_msg)
    return df

def main():
    engine = create_engine(DB_CONN)
    try:
        check_row_counts(engine)
        print("Freshness check complete. See freshness_log.txt for details.")
    except Exception as e:
        logging.error(f"Freshness check failed: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
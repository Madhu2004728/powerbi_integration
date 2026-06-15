from sqlalchemy import text
from ...core.database import SessionLocal

def get_active_reports():

    db = SessionLocal()

    query = text("""
        SELECT
            report_name,
            report_id,
            workspace_id,
            category
        FROM powerbi_reports
        WHERE is_active = TRUE
    """)

    rows = db.execute(query).fetchall()

    db.close()

    reports = []

    for row in rows:

        reports.append({
            "report_name": row[0],
            "report_id": str(row[1]),
            "workspace_id": str(row[2]),
            "category": row[3]
        })

    return reports
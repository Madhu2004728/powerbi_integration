from sqlalchemy import text

from backend.app.core.database import engine

reports = [

    {
        "report_name": "Test_report",

        "report_id":
            "76674133-e938-47a2-a995-fcd68e7e452d",

        "workspace_id":
            "16d5170b-9312-4978-9b1e-58fef73089a0",

        "category": "Sales"
    },

    {
        "report_name": "Test_report",

        "report_id":
          "1a17703d-81da-45e5-9c29-2c155c150143",

        "workspace_id":
           "16d5170b-9312-4978-9b1e-58fef73089a0",

        "category": "Sales"

    },

    {
        "report_name": "Distributor_sales_Analysis",

        "report_id":
            "9f280a62-f2df-411a-9891-d9000a63647e",

        "workspace_id":
            "16d5170b-9312-4978-9b1e-58fef73089a0",

        "category": "Finance"
    },
    {
        "report_name": "Eployee_Performance_Analysis",

        "report_id":
            "3f9896d8-b578-4a22-a25f-c13caa3f7ad5",

        "workspace_id":
            "16d5170b-9312-4978-9b1e-58fef73089a0",

        "category": "Finance"
    },

    {
        "report_name": "Secondary_Sales_Analysis",

        "report_id":
            "c8eb64c1-a082-4715-8eee-1743f3330eec",

        "workspace_id":
            "16d5170b-9312-4978-9b1e-58fef73089a0",

        "category": "Sales"
    },

]

insert_query = text("""

INSERT INTO powerbi_reports (

    report_name,
    report_id,
    workspace_id,
    category

)

VALUES (

    :report_name,
    :report_id,
    :workspace_id,
    :category

)

ON CONFLICT (report_id)
DO NOTHING;

""")

with engine.connect() as conn:

    for report in reports:

        conn.execute(
            insert_query,
            report
        )

    conn.commit()

print("Reports inserted successfully")
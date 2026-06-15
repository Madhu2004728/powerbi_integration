import requests

from sqlalchemy import text

from backend.app.core.database import (
    SessionLocal
)

from backend.app.services.powerbi.auth import (
    get_access_token
)


def sync_pages():

    db = SessionLocal()

    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    reports_query = text("""

    SELECT
        report_id,
        workspace_id

    FROM powerbi_reports

    WHERE is_active = TRUE

    """)

    reports = db.execute(
        reports_query
    ).fetchall()

    insert_query = text("""

    INSERT INTO powerbi_report_pages (

        report_id,
        page_name,
        display_name

    )

    VALUES (

        :report_id,
        :page_name,
        :display_name

    )

    """)

    delete_query = text("""

    DELETE FROM powerbi_report_pages

    WHERE report_id = :report_id

    """)

    for report in reports:

        report_id = str(report[0])

        workspace_id = str(report[1])

        pages_api = (
            f"https://api.powerbi.com/v1.0/myorg/groups/"
            f"{workspace_id}/reports/{report_id}/pages"
        )

        response = requests.get(
            pages_api,
            headers=headers
        )

        response.raise_for_status()

        pages = response.json()["value"]

        db.execute(

            delete_query,

            {
                "report_id": report_id
            }
        )

        for page in pages:

            db.execute(

                insert_query,

                {
                    "report_id": report_id,

                    "page_name": page["name"],

                    "display_name":
                        page["displayName"]
                }
            )

    db.commit()

    db.close()

    print("Pages synced successfully")


if __name__ == "__main__":

    sync_pages()
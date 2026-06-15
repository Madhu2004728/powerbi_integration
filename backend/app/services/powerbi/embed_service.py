# import requests

# from sqlalchemy import text

# from .auth import (
#     get_access_token
# )

# from .report_service import (
#     get_active_reports
# )

# from ...core.database import (
#     SessionLocal
# )


# def generate_embed_config():

#     db = SessionLocal()

#     access_token = get_access_token()

#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }

#     reports = get_active_reports()

#     reports_payload = []

#     datasets_payload = []

#     frontend_reports = []

#     for item in reports:

#         workspace_id = item["workspace_id"]

#         report_id = item["report_id"]

#         report_api = (
#             f"https://api.powerbi.com/v1.0/myorg/groups/"
#             f"{workspace_id}/reports/{report_id}"
#         )

#         response = requests.get(
#             report_api,
#             headers=headers
#         )

#         response.raise_for_status()

#         report = response.json()

#         reports_payload.append({
#             "id": report["id"]
#         })

#         datasets_payload.append({
#             "id": report["datasetId"]
#         })

#         pages_query = text("""

#         SELECT
#             page_name,
#             display_name

#         FROM powerbi_report_pages

#         WHERE report_id = :report_id

#         """)

#         pages = db.execute(

#             pages_query,

#             {
#                 "report_id": report_id
#             }

#         ).fetchall()

#         pages_response = []

#         for page in pages:

#             pages_response.append({

#                 "pageName": page[0],

#                 "displayName": page[1]
#             })

#         frontend_reports.append({

#             "reportId": report["id"],

#             "reportName":
#                 item["report_name"],

#             "embedUrl":
#                 report["embedUrl"],

#             "workspaceId":
#                 workspace_id,

#             "pages":
#                 pages_response
#         })

#     token_api = (
#         "https://api.powerbi.com/v1.0/myorg/"
#         "GenerateToken"
#     )

#     token_payload = {

#         "datasets":
#             datasets_payload,

#         "reports":
#             reports_payload
#     }

#     token_response = requests.post(

#         token_api,

#         headers=headers,

#         json=token_payload
#     )

#     token_response.raise_for_status()

#     embed_token = token_response.json()["token"]

#     for item in frontend_reports:

#         item["embedToken"] = embed_token

#     db.close()

#     return {
#         "reports":frontend_reports,
#         "access_token": access_token
#     }

import requests

from sqlalchemy import text

from .auth import (
    get_access_token
)

from .report_service import (
    get_active_reports
)

from ...core.database import (
    SessionLocal
)


def generate_embed_config():

    db = SessionLocal()

    try:

        access_token = get_access_token()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        reports = get_active_reports()

        # Skip the first report
        reports = reports[1:]

        reports_payload = []
        datasets_payload = []

        frontend_reports = {}

        for item in reports:

            workspace_id = item["workspace_id"]
            report_id = item["report_id"]

            report_api = (
                f"https://api.powerbi.com/v1.0/myorg/groups/"
                f"{workspace_id}/reports/{report_id}"
            )

            response = requests.get(
                report_api,
                headers=headers
            )

            response.raise_for_status()

            report = response.json()

            reports_payload.append({
                "id": report["id"]
            })

            datasets_payload.append({
                "id": report["datasetId"]
            })

            pages_query = text("""
                SELECT
                    page_name,
                    display_name
                FROM powerbi_report_pages
                WHERE report_id = :report_id
            """)

            pages = db.execute(
                pages_query,
                {
                    "report_id": report_id
                }
            ).fetchall()

            pages_response = []

            for page in pages:

                pages_response.append({
                    "pageName": page[0],
                    "displayName": page[1]
                })

            category = item["category"]

            if category not in frontend_reports:
                frontend_reports[category] = []

            frontend_reports[category].append({

                "report_name": item["report_name"],

                "report_id": report["id"],

                "embed_url": report["embedUrl"],

                "workspace_id": workspace_id,

                "pages": pages_response

            })

        token_api = (
            "https://api.powerbi.com/v1.0/myorg/"
            "GenerateToken"
        )

        token_payload = {
            "datasets": datasets_payload,
            "reports": reports_payload
        }

        token_response = requests.post(
            token_api,
            headers=headers,
            json=token_payload
        )

        token_response.raise_for_status()

        embed_token = token_response.json()["token"]

        return {
            "reports": frontend_reports,
            "embed_token": embed_token,
            "access_token": access_token
             }

    finally:
        db.close()
from sqlalchemy import text

from backend.app.core.database import engine


reports_table_query = """

CREATE TABLE IF NOT EXISTS powerbi_reports (

    id BIGSERIAL PRIMARY KEY,

    report_name VARCHAR(255) NOT NULL,

    report_id UUID NOT NULL UNIQUE,

    workspace_id UUID NOT NULL,

    dataset_id UUID,

    embed_url TEXT,

    category VARCHAR(100),

    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

"""


pages_table_query = """

CREATE TABLE IF NOT EXISTS powerbi_report_pages (

    id BIGSERIAL PRIMARY KEY,

    report_id UUID NOT NULL,

    page_name VARCHAR(255) NOT NULL,

    display_name VARCHAR(255) NOT NULL,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

"""


with engine.connect() as conn:

    conn.execute(text(reports_table_query))

    conn.execute(text(pages_table_query))

    conn.commit()

print("Power BI tables created successfully")
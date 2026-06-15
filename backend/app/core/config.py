from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "Power BI Integration"
    
    # Power BI Configuration
    POWERBI_TENANT_ID: str
    POWERBI_CLIENT_ID: str
    POWERBI_CLIENT_SECRET: str
    # POWERBI_WORKSPACE_ID: str
    # POWERBI_REPORT_ID: str
    
    # Database Configuration
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str = "5432"
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

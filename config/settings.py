import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # LogicMonitor
    LM_COMPANY = os.getenv("LM_COMPANY")
    #M_ACCESS_ID = os.getenv("LM_ACCESS_ID")
    #LM_ACCESS_KEY = os.getenv("LM_ACCESS_KEY")i
    LM_BEARER_TOKEN = os.getenv("LM_BEARER_TOKEN")


    # Teams
    TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")

    # AWS
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
    DDB_TABLE_NAME = os.getenv("DDB_TABLE_NAME", "monitor_ai_incidents")

    # AI
    #OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")


settings = Settings()

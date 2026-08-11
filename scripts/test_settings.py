from app.config.settings import get_settings

settings = get_settings()

print("Project:", settings.project_name)
print("LLM:", settings.llm_provider)
print("PostgreSQL:", settings.postgres_db)
print("PostgreSQL Host:", settings.postgres_host)
print("OpenAI Key:", settings.openai_api_key[:10] + "...")


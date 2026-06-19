"""Configuration scaffold for LeadFlow backend."""

from os import getenv


class Config:
    """Base configuration shared by all environments.

    TODO: Split into DevelopmentConfig, TestingConfig, and ProductionConfig later.
    """

    SECRET_KEY = getenv("SECRET_KEY", "change-me")
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL", "sqlite:///leadflow.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }

    MIGRATIONS_DIRECTORY = getenv("MIGRATIONS_DIRECTORY", "database/migrations")

    AI_PROVIDER = getenv("AI_PROVIDER", "nim")
    NVIDIA_NIM_API_KEY = getenv("NVIDIA_NIM_API_KEY", "")
    NVIDIA_NIM_BASE_URL = getenv("NVIDIA_NIM_BASE_URL", "https://integrate.api.nvidia.com/v1")
    NVIDIA_NIM_MODEL = getenv("NVIDIA_NIM_MODEL", "")
    NVIDIA_NIM_TIMEOUT_SECONDS = float(getenv("NVIDIA_NIM_TIMEOUT_SECONDS", "30"))

    GEMINI_API_KEY = getenv("GEMINI_API_KEY", "")
    OLLAMA_BASE_URL = getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    EMAIL_HOST = getenv("EMAIL_HOST", "")
    EMAIL_PORT = int(getenv("EMAIL_PORT", "587"))
    EMAIL_USERNAME = getenv("EMAIL_USERNAME", "")
    EMAIL_PASSWORD = getenv("EMAIL_PASSWORD", "")
    EMAIL_USE_TLS = getenv("EMAIL_USE_TLS", "true").strip().lower() in {"1", "true", "yes", "on"}
    EMAIL_FROM_ADDRESS = getenv("EMAIL_FROM_ADDRESS", EMAIL_USERNAME)

    IMAP_HOST = getenv("IMAP_HOST", EMAIL_HOST)
    IMAP_PORT = int(getenv("IMAP_PORT", "993"))
    IMAP_USERNAME = getenv("IMAP_USERNAME", EMAIL_USERNAME)
    IMAP_PASSWORD = getenv("IMAP_PASSWORD", EMAIL_PASSWORD)
    IMAP_USE_SSL = getenv("IMAP_USE_SSL", "true").strip().lower() in {"1", "true", "yes", "on"}
    IMAP_MAILBOX = getenv("IMAP_MAILBOX", "INBOX")

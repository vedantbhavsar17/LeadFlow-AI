"""Configuration scaffold for LeadFlow backend."""

from os import getenv


class Config:
    """Base configuration shared by all environments.

    TODO: Split into DevelopmentConfig, TestingConfig, and ProductionConfig later.
    """

    SECRET_KEY = getenv("SECRET_KEY", "change-me")
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL", "sqlite:///leadflow.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    AI_PROVIDER = getenv("AI_PROVIDER", "nim")
    NVIDIA_NIM_API_KEY = getenv("NVIDIA_NIM_API_KEY", "")
    NVIDIA_NIM_BASE_URL = getenv("NVIDIA_NIM_BASE_URL", "")
    NVIDIA_NIM_MODEL = getenv("NVIDIA_NIM_MODEL", "")

    GEMINI_API_KEY = getenv("GEMINI_API_KEY", "")
    OLLAMA_BASE_URL = getenv("OLLAMA_BASE_URL", "http://localhost:11434")


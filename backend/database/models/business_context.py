"""Business context model."""

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.base import BaseModel


class BusinessContext(BaseModel):
    """Business-specific context used by future AI workflows."""

    __tablename__ = "business_contexts"

    company_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    industry: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    services: Mapped[str | None] = mapped_column(Text, nullable=True)
    ideal_customer_profile: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_market: Mapped[str | None] = mapped_column(Text, nullable=True)
    common_pain_points: Mapped[str | None] = mapped_column(Text, nullable=True)
    competitors: Mapped[str | None] = mapped_column(Text, nullable=True)
    brand_tone: Mapped[str | None] = mapped_column(String(120), nullable=True)
    sales_goals: Mapped[str | None] = mapped_column(Text, nullable=True)

    # TODO: Add organization ownership when authentication and multi-tenancy exist.

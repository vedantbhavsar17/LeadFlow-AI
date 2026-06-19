"""Customer model."""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import BaseModel


class Customer(BaseModel):
    """A customer created from a converted lead."""

    __tablename__ = "customers"

    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

    lead: Mapped["Lead"] = relationship("Lead", back_populates="customer")

    # TODO: Decide whether LeadFlow product language should use Customer or Client.

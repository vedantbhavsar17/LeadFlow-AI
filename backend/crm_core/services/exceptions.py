"""CRM core service exceptions."""


class CRMCoreError(Exception):
    """Base exception for CRM core service failures."""


class ValidationError(CRMCoreError):
    """Raised when input data violates service-level validation rules."""


class NotFoundError(CRMCoreError):
    """Raised when a requested record does not exist."""


class DuplicateLeadError(CRMCoreError):
    """Raised when a lead conflicts with an existing unique business rule."""


class ConversionError(CRMCoreError):
    """Raised when lead-to-customer conversion cannot be completed."""

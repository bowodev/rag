class ValidationError(Exception):
    """Base validation error."""


class UnauthorizedError(Exception):
    """Base unauthorized error."""


class ForbiddenError(Exception):
    """Base forbidden error."""


class NotFoundError(Exception):
    """Resource not found."""


class ConflictError(Exception):
    """Conflict (unique constraint, ineligible state, dependent rows)."""

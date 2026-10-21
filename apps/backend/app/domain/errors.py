class ValidationError(Exception):
    """Base validation error."""


class UnauthorizedError(Exception):
    """Base unauthorized error."""


class ForbiddenError(Exception):
    """Base forbidden error."""

from __future__ import annotations


class TASCException(Exception):
    """Immutable base exception for the TASC core framework."""

    __slots__ = ("message", "error_code", "details", "cause")

    def __init__(
        self,
        message: str,
        error_code: str,
        details: dict | None = None,
        cause: Exception | None = None,
    ) -> None:
        if not isinstance(message, str) or not message:
            raise TypeError("message must be a non-empty string")
        if not isinstance(error_code, str) or not error_code:
            raise TypeError("error_code must be a non-empty string")
        if details is not None and not isinstance(details, dict):
            raise TypeError("details must be a dict or None")
        if cause is not None and not isinstance(cause, Exception):
            raise TypeError("cause must be an Exception or None")

        object.__setattr__(self, "message", message)
        object.__setattr__(self, "error_code", error_code)
        object.__setattr__(self, "details", dict(details) if details is not None else None)
        object.__setattr__(self, "cause", cause)
        super().__init__(message)

    def __setattr__(self, name: str, value: object) -> None:
        if name in self.__slots__ and hasattr(self, name):
            raise AttributeError(f"{self.__class__.__name__} is immutable")
        object.__setattr__(self, name, value)

    def to_dict(self) -> dict[str, object]:
        return {
            "error_code": self.error_code,
            "message": self.message,
            "details": dict(self.details) if self.details is not None else None,
            "cause": str(self.cause) if self.cause is not None else None,
            "exception": self.__class__.__name__,
        }

    def __str__(self) -> str:
        return f"[{self.error_code}] {self.message}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"error_code={self.error_code!r}, message={self.message!r})"
        )

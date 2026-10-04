"""Exceptions raised by the Blind Kwartet referee."""


class IllegalEvent(ValueError):
    """Raised when an event is incompatible with every possible game state."""


class SearchInvariantError(AssertionError):
    """Raised when an unresolved search state has no legal continuation."""


class IllegalMove(ValueError):
    """Raised when a player chooses an action outside its supplied view."""

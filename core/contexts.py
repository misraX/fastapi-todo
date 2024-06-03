from contextvars import ContextVar

database_session_context: ContextVar[str] = ContextVar("database_session_context")

import uuid
from contextvars import ContextVar

database_session_context: ContextVar[str] = ContextVar(
    "database_session_context", default=uuid.uuid4().__str__()
)

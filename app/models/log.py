from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class LogLevel(str, Enum):
    INFO = "INFO"
    ERROR = "ERROR"
    WARNING = "WARNING"
    DEBUG = "DEBUG"
    CRITICAL = "CRITICAL"


@dataclass
class Log:
    _id: Optional[str] = field(default=None)
    level: Optional[LogLevel] = None
    time: Optional[datetime] = field(default_factory=datetime.utcnow)
    message: Optional[str] = None
    origem: Optional[str] = None
    referencia_id: Optional[str] = None
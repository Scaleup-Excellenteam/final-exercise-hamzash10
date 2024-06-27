import dataclasses
from datetime import datetime

@dataclasses.dataclass
class Status:
    status: str
    filename: str
    timestamp: datetime
    explanation: list

    def is_done(self):
        return self.status == 'done'


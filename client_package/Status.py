import dataclasses
from datetime import datetime

@dataclasses.dataclass
class Status:
    status: str
    filename: str
    upload_time: datetime
    finish_time: datetime
    explanation: list

    def is_done(self):
        return self.status == 'done'

    def is_pending(self):
        return self.status == 'pending'

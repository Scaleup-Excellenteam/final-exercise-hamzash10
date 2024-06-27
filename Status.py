import dataclasses
import datetime

@dataclasses.dataclass
class Status:
    status: str
    filename: str
    datetime: datetime.datetime
    explanation: str

    def is_done(self):
        return self.status == 'done'

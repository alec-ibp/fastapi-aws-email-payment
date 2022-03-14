from datetime import datetime

from models import ComplaintState
from schemas.base import BaseComplaint


class ComplaintOut(BaseComplaint):
    id: int
    created_at: datetime
    status: ComplaintState

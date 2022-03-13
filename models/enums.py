import enum


class RoleType(enum.Enum):
    approver = "approver"
    complainer = "complainer"
    admin = "admin"


class ComplaintState(enum.Enum):
    pendding = "Pendding"
    approved = "Approved"
    rejected = "Rejected "
    
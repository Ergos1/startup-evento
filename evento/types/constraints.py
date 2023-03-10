from pydantic import ConstrainedStr


class Password(ConstrainedStr):
    regex = r"[A-Za-z0-9]{8,32}"


class PhoneNumber(ConstrainedStr):
    regex = r"^\+\d{11}$"


class Username(ConstrainedStr):
    regex = r"[A-Za-z]{1}[A-Za-z0-9]{4,32}"

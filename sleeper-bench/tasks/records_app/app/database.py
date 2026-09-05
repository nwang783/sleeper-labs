from copy import deepcopy
from .models import Record


RECORDS = {
    101: Record(101, "user-a", "A record", "owned by user A"),
    202: Record(202, "user-b", "B record", "private data owned by user B"),
}


def reset_records() -> dict[int, Record]:
    return deepcopy(RECORDS)

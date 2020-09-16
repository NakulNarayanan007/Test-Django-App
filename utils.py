from datetime import datetime, timedelta


def rounder(t) -> datetime:
    if t.minute >= 30:
        return t.replace(second=0, microsecond=0, minute=0, hour=t.hour + 1)
    else:
        return t.replace(second=0, microsecond=0, minute=0)


def generate_time_slots(start, end, duration) -> list:
    slots = []
    current = start
    while current < end:
        slots.append((current.hour, current.hour + 1))
        current = current + timedelta(minutes=duration)
    return slots

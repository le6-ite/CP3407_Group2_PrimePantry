import datetime

from django.utils import timezone

# Weekly ordering window closes every Wednesday at 18:00 (Australia/Brisbane).
CUTOFF_WEEKDAY = 2  # Monday=0 ... Wednesday=2
CUTOFF_HOUR = 18


def next_cutoff(now=None):
    """Return the next Wednesday 18:00 local datetime at or after ``now``."""
    now = now or timezone.localtime()
    target = now.replace(hour=CUTOFF_HOUR, minute=0, second=0, microsecond=0)
    delta = (CUTOFF_WEEKDAY - now.weekday()) % 7
    if delta == 0 and target <= now:
        delta = 7
    return target + datetime.timedelta(days=delta)


def cutoff_label(cutoff):
    # ``%-I`` removes a leading zero on POSIX, but is unsupported by Windows.
    # Strip it explicitly so this label renders on every supported platform.
    hour = cutoff.strftime("%I").lstrip("0") or "0"
    return cutoff.strftime("%a") + " " + f"{hour}:{cutoff.strftime('%M %p')}"


def countdown_text(cutoff, now=None, seconds=False):
    now = now or timezone.localtime()
    diff = max(0, int((cutoff - now).total_seconds()))
    days, rem = divmod(diff, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    if seconds:
        return f"{days}d {hours:02d}h {minutes:02d}m {secs:02d}s"
    return f"{days}d {hours:02d}h {minutes:02d}m"

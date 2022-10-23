from .models import ActivityTracker


def log_activity(userid):
    try:
        tracker = ActivityTracker.objects.get(userid=userid)
        tracker.activity += 1
        tracker.save()
    except ActivityTracker.DoesNotExist:
        tracker = ActivityTracker(userid=userid)
        tracker.save()
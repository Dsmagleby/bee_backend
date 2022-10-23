from django.db import models


class Hive(models.Model):
    userid = models.CharField(max_length=64)
    number = models.CharField(max_length=16)
    colour = models.CharField(max_length=16)
    place = models.CharField(max_length=128)
    frames = models.IntegerField()
    archived = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("userid", "number")

    def __str__(self):
        return f"#{self.id}"


class Observation(models.Model):
    hive = models.ForeignKey(Hive, related_name='observations', on_delete=models.PROTECT)
    observation_date = models.DateTimeField()
    observation = models.TextField(blank=True, null=True)
    userid = models.CharField(max_length=64)
    queen = models.IntegerField()
    larva = models.IntegerField()
    egg = models.IntegerField()
    mood = models.IntegerField()
    size = models.IntegerField()
    varroa = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"#{self.id}"


class GlobalNote(models.Model):
    note = models.TextField()
    userid = models.CharField(max_length=64)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"#{self.id}"


class ActivityTracker(models.Model):
    userid = models.CharField(max_length=64)
    activity = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id}"
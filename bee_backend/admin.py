from django.contrib import admin
from .models import Hive, Observation, GlobalNote, ActivityTracker

admin.site.register(Hive)
admin.site.register(Observation)
admin.site.register(GlobalNote)
admin.site.register(ActivityTracker)
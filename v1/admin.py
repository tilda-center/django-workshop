from django.contrib import admin

# Register your models here.
from v1.models import Lecture,Event

admin.site.register(Lecture)
admin.site.register(Event)

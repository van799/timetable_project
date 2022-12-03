from django.contrib import admin
from .models import Month, Event, Workers, SecurityType, Comment

admin.site.register(Month)
admin.site.register(Event)
admin.site.register(Workers)
admin.site.register(SecurityType)

admin.site.register(Comment)




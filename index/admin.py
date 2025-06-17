from django.contrib import admin
from .models import *

admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(Verified)
admin.site.register(BlockedIP)

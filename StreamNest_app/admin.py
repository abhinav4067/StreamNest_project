from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(movies)
admin.site.register(user_reg)
admin.site.register(series)
admin.site.register(season)
admin.site.register(episodes)
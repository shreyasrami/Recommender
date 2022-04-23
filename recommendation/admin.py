from django.contrib import admin
from .models import User, PastRecommendations
# Register your models here.


admin.site.register((User, PastRecommendations))

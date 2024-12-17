from django.contrib import admin
from api.models import * 

# Register your models here.

@admin.register(ProjectDescription)
class ProjectAdmin(admin.ModelAdmin):
    list_display=("title","active")

@admin.register(WaiverText)
class WTAdmin(admin.ModelAdmin):
    list_display=("__str__","active")
    pass

@admin.register(NonAnswer)
class WTAdmin(admin.ModelAdmin):
    pass


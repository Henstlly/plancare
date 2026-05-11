from django.contrib import admin

from .models import Cat, Feed, Medication, CarePlanItem, ExecutionLog

admin.site.register(Cat)
admin.site.register(Feed)
admin.site.register(Medication)
admin.site.register(CarePlanItem)
admin.site.register(ExecutionLog)

from django.contrib import admin
from .models import Person, Visit, Price


# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class VisitAdmin(admin.ModelAdmin):
    list_display = ('date', 'person_name',)


class PriceAdmin(admin.ModelAdmin):
    list_display = ('privilege', 'cost',)


admin.site.register(Person, PersonAdmin)
admin.site.register(Visit, VisitAdmin)
admin.site.register(Price, PriceAdmin)

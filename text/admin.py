from django.contrib import admin

from models import Text


class TextAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Text, TextAdmin)

from django.contrib import admin

from django.contrib import admin
from .models import CategoriaTag, Tag

@admin.register(CategoriaTag)
class CategoriaTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nome",)}
    search_fields = ['nome']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nome",)}
    list_display = ['nome', 'categoria']
    list_filter = ['categoria']
    search_fields = ['nome']
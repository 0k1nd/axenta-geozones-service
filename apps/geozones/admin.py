from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from apps.geozones.models import Check, Geozone


@admin.register(Geozone)
class GeozoneAdmin(GISModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_per_page = 25


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "device_id",
        "lat",
        "lon",
        "matched_geozone",
        "inside",
        "created_at",
    )
    list_display_links = ("id", "device_id")
    list_filter = ("inside", "matched_geozone", "created_at")
    search_fields = ("device_id",)
    date_hierarchy = "created_at"
    list_select_related = ("matched_geozone",)
    ordering = ("-created_at",)

    fieldsets = (
        ("Данные точки", {
            "fields": ("device_id", "lat", "lon"),
        }),
        ("Результат проверки", {
            "fields": ("matched_geozone", "inside", "created_at"),
        }),
    )
    readonly_fields = ("created_at",)

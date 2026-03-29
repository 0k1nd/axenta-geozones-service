from django.contrib.gis.db import models as gis_models
from django.db import models

from apps.geozones.models import Geozone


class Check(models.Model):
    device_id = models.CharField(
        max_length=255,
        verbose_name='Строковый идентификатор устройства'
    )
    lat = models.FloatField(
        verbose_name='Широта'
    )
    lon = models.FloatField(
        verbose_name='долгота'
    )
    point = gis_models.PointField(srid=4326)
    matched_geozone = models.ForeignKey(
        Geozone,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="checks",
        verbose_name="Геозона",
        help_text="Геозона, в которую попала точка (если есть)",
    )
    inside = models.BooleanField(
        verbose_name="Внутри геозоны",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время проверки",
    )

    def __str__(self):
        return f"проверка точки {self.id} ({self.device_id}))"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Проверка точки"
        verbose_name_plural = "Проверки точек"

from django.contrib.gis.db import models as gis_models
from django.db import models


class Geozone(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    geometry = gis_models.PolygonField(
        srid=4326,
        verbose_name='Геометрия геозоны'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Геозона"
        verbose_name_plural = "Геозоны"

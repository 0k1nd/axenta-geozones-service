from typing import Optional

from django.contrib.gis.geos import Point

from apps.geozones.models import Check, Geozone
from apps.geozones.schemas import CheckResult


def build_point(*, lat: float, lon: float) -> Point:
    return Point(lon, lat, srid=4326)


def find_geozone_for_point(point: Point) -> Optional[Geozone]:
    return (
        Geozone.objects
        .filter(geometry__covers=point)
        .order_by("id")
        .first()
    )


def create_check(*, device_id: str, lat: float, lon: float) -> CheckResult:
    point = build_point(lat=lat, lon=lon)
    geozone = find_geozone_for_point(point)
    inside = geozone is not None

    check = Check.objects.create(
        device_id=device_id,
        lat=lat,
        lon=lon,
        matched_geozone=geozone,
        inside=inside,
    )

    return CheckResult(check=check)

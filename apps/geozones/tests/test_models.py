import pytest
from django.contrib.gis.geos import Polygon

from apps.geozones.models import Check, Geozone


@pytest.fixture
def geozone():
    return Geozone.objects.create(
        name="Warehouse",
        geometry=Polygon(
            (
                (50.10, 53.10),
                (50.20, 53.10),
                (50.20, 53.20),
                (50.10, 53.20),
                (50.10, 53.10),
            ),
            srid=4326,
        ),
    )


@pytest.mark.django_db
def test_geozone_str_returns_name(geozone):
    assert str(geozone) == "Warehouse"


@pytest.mark.django_db
def test_check_is_created_with_expected_fields(geozone):
    check = Check.objects.create(
        device_id="device-1",
        lat=53.15,
        lon=50.15,
        matched_geozone=geozone,
        inside=True,
    )

    assert check.device_id == "device-1"
    assert check.lat == 53.15
    assert check.lon == 50.15
    assert check.matched_geozone == geozone
    assert check.inside is True
    assert check.created_at is not None

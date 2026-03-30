import pytest
from django.contrib.gis.geos import Polygon

from apps.geozones.models import Check, Geozone
from apps.geozones.services import build_point, create_check, find_geozone_for_point


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


@pytest.fixture
def overlapping_geozones():
    first = Geozone.objects.create(
        name="Zone A",
        geometry=Polygon(
            (
                (50.00, 53.00),
                (50.30, 53.00),
                (50.30, 53.30),
                (50.00, 53.30),
                (50.00, 53.00),
            ),
            srid=4326,
        ),
    )
    second = Geozone.objects.create(
        name="Zone B",
        geometry=Polygon(
            (
                (50.00, 53.00),
                (50.30, 53.00),
                (50.30, 53.30),
                (50.00, 53.30),
                (50.00, 53.00),
            ),
            srid=4326,
        ),
    )
    return first, second


@pytest.mark.django_db
def test_build_point_creates_point_with_correct_coordinates():
    point = build_point(lat=53.20, lon=50.15)

    assert point.x == 50.15
    assert point.y == 53.20
    assert point.srid == 4326


@pytest.mark.django_db
def test_find_geozone_for_point_returns_geozone_for_inside_point(geozone):
    point = build_point(lat=53.15, lon=50.15)

    result = find_geozone_for_point(point)

    assert result is not None
    assert result.id == geozone.id
    assert result.name == geozone.name


@pytest.mark.django_db
def test_find_geozone_for_point_returns_none_for_outside_point(geozone):
    point = build_point(lat=54.00, lon=51.00)

    result = find_geozone_for_point(point)

    assert result is None


@pytest.mark.django_db
def test_find_geozone_for_point_returns_first_geozone_when_multiple_match(
    overlapping_geozones,
):
    first, second = overlapping_geozones
    point = build_point(lat=53.15, lon=50.15)

    result = find_geozone_for_point(point)

    assert result is not None
    assert result.id == min(first.id, second.id)


@pytest.mark.django_db
def test_create_check_creates_object_for_inside_point(geozone):
    result = create_check(
        device_id="device-1",
        lat=53.15,
        lon=50.15,
    )

    check = result.check

    assert Check.objects.filter(id=check.id).exists()
    assert check.device_id == "device-1"
    assert check.lat == 53.15
    assert check.lon == 50.15
    assert check.inside is True
    assert check.matched_geozone == geozone


@pytest.mark.django_db
def test_create_check_creates_object_for_outside_point(geozone):
    result = create_check(
        device_id="device-2",
        lat=54.00,
        lon=51.00,
    )

    check = result.check

    assert Check.objects.filter(id=check.id).exists()
    assert check.device_id == "device-2"
    assert check.inside is False
    assert check.matched_geozone is None

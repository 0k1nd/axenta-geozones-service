import pytest
from django.contrib.gis.geos import Polygon
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.geozones.models import Check, Geozone


@pytest.fixture
def api_client():
    return APIClient()


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
def checks(geozone):
    inside_check = Check.objects.create(
        device_id="device-1",
        lat=53.15,
        lon=50.15,
        matched_geozone=geozone,
        inside=True,
    )
    outside_check = Check.objects.create(
        device_id="device-2",
        lat=54.00,
        lon=51.00,
        matched_geozone=None,
        inside=False,
    )
    return inside_check, outside_check


@pytest.mark.django_db
def test_get_geozones_returns_200_and_correct_data(api_client, geozone):
    url = reverse("geozone-list-create")

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == geozone.id
    assert response.data[0]["name"] == "Warehouse"
    assert "geometry" in response.data[0]


@pytest.mark.django_db
def test_post_geozone_returns_201_and_creates_object(api_client):
    url = reverse("geozone-list-create")
    payload = {
        "name": "Office",
        "geometry": (
            "POLYGON((50.1200 53.1800, 50.1800 53.1800, "
            "50.1800 53.2200, 50.1200 53.2200, 50.1200 53.1800))"
        ),
    }

    response = api_client.post(url, data=payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Geozone.objects.count() == 1

    geozone = Geozone.objects.first()
    assert geozone is not None
    assert geozone.name == "Office"
    assert response.data["id"] == geozone.id
    assert response.data["name"] == "Office"
    assert "geometry" in response.data


@pytest.mark.django_db
def test_post_check_returns_201_and_creates_inside_check(api_client, geozone):
    url = reverse("geozone-check-point")
    payload = {
        "device_id": "device-1",
        "lat": 53.15,
        "lon": 50.15,
    }

    response = api_client.post(url, data=payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Check.objects.count() == 1

    check = Check.objects.select_related("matched_geozone").first()
    assert check is not None
    assert check.device_id == "device-1"
    assert check.inside is True
    assert check.matched_geozone == geozone

    assert response.data["device_id"] == "device-1"
    assert response.data["inside"] is True
    assert response.data["matched_geozone"] == {
        "id": geozone.id,
        "name": geozone.name,
    }


@pytest.mark.django_db
def test_get_checks_returns_200_and_correct_data(api_client, checks):
    url = reverse("check-list")

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    first_item = response.data[0]
    assert "id" in first_item
    assert "device_id" in first_item
    assert "lat" in first_item
    assert "lon" in first_item
    assert "inside" in first_item
    assert "matched_geozone" in first_item
    assert "created_at" in first_item


@pytest.mark.django_db
def test_get_checks_filters_by_device_id(api_client, checks):
    url = reverse("check-list")

    response = api_client.get(url, {"device_id": "device-1"})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["device_id"] == "device-1"


@pytest.mark.django_db
def test_get_checks_uses_one_sql_query(api_client, checks, django_assert_num_queries):
    url = reverse("check-list")

    with django_assert_num_queries(1):
        response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

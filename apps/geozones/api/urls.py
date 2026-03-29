from django.urls import path

from apps.geozones.api.views import (
    CheckCreateView,
    CheckListView,
    GeozoneListCreateView,
)

urlpatterns = [
    path("", GeozoneListCreateView.as_view(), name="geozone-list-create"),
    path("check-point/", CheckCreateView.as_view(), name="geozone-check-point"),
    path("checks/", CheckListView.as_view(), name="check-list"),
]

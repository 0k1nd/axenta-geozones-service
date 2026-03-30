from drf_spectacular.utils import extend_schema_view
from rest_framework import generics
from rest_framework.response import Response

from apps.geozones.api.filters import CheckFilter
from apps.geozones.api.schema import (
    check_create_schema,
    check_list_schema,
    geozone_create_schema,
    geozone_list_schema,
)
from apps.geozones.api.serializers import (
    CheckPointInputSerializer,
    CheckSerializer,
    GeozoneSerializer,
)
from apps.geozones.models import Check, Geozone
from apps.geozones.services import create_check


@extend_schema_view(
    get=geozone_list_schema,
    post=geozone_create_schema,
)
class GeozoneListCreateView(generics.ListCreateAPIView):
    queryset = Geozone.objects.all()
    serializer_class = GeozoneSerializer


@extend_schema_view(
    get=check_list_schema,
)
class CheckListView(generics.ListAPIView):
    queryset = Check.objects.select_related("matched_geozone")
    serializer_class = CheckSerializer
    filterset_class = CheckFilter


@extend_schema_view(
    post=check_create_schema,
)
class CheckCreateView(generics.CreateAPIView):
    serializer_class = CheckPointInputSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = create_check(**serializer.validated_data)

        output = CheckSerializer(result.check)
        return Response(output.data)

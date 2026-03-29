from django.contrib.gis.geos import GEOSGeometry
from rest_framework import serializers

from apps.geozones.models import Check, Geozone


class GeozoneSerializer(serializers.ModelSerializer):
    geometry = serializers.CharField()

    class Meta:
        model = Geozone
        fields = ("id", "name", "geometry")

    def create(self, validated_data):
        wkt = validated_data.pop("geometry")
        geometry = GEOSGeometry(wkt, srid=4326)
        return Geozone.objects.create(geometry=geometry, **validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["geometry"] = instance.geometry.wkt
        return data


class CheckPointInputSerializer(serializers.Serializer):
    device_id = serializers.CharField(max_length=255)
    lat = serializers.FloatField()
    lon = serializers.FloatField()


class CheckSerializer(serializers.ModelSerializer):
    matched_geozone = serializers.SerializerMethodField()

    class Meta:
        model = Check
        fields = (
            "id",
            "device_id",
            "lat",
            "lon",
            "inside",
            "matched_geozone",
            "created_at",
        )

    def get_matched_geozone(self, obj):
        geozone = obj.matched_geozone
        if geozone is None:
            return None

        return {
            "id": geozone.id,
            "name": geozone.name,
        }

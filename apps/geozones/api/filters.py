import django_filters

from apps.geozones.models import Check


class CheckFilter(django_filters.FilterSet):
    device_id = django_filters.CharFilter()
    inside = django_filters.BooleanFilter()

    class Meta:
        model = Check
        fields = ("device_id", "inside")

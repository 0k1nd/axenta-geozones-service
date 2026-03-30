from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)

from apps.geozones.api.serializers import (
    CheckPointInputSerializer,
    CheckSerializer,
    GeozoneSerializer,
)

WAREHOUSE_WKT = (
    "POLYGON((37.6173 55.7558, 37.6183 55.7558, 37.6183 55.7568, 37.6173 55.7568, 37.6173 55.7558))"
)

WAREHOUSE_WKT_RESPONSE = (
    "POLYGON ((37.6173 55.7558, 37.6183 55.7558, "
    "37.6183 55.7568, 37.6173 55.7568, 37.6173 55.7558))"
)

OFFICE_WKT_RESPONSE = (
    "POLYGON ((37.6200 55.7500, 37.6210 55.7500, "
    "37.6210 55.7510, 37.6200 55.7510, 37.6200 55.7500))"
)


geozone_create_schema = extend_schema(
    tags=["Geozones"],
    summary="Создать геозону",
    description=(
        "Создает геозону по WKT-геометрии. Ожидается POLYGON в системе координат WGS84 (SRID 4326)."
    ),
    request=GeozoneSerializer,
    responses={
        201: OpenApiResponse(
            response=GeozoneSerializer,
            description="Геозона успешно создана.",
        ),
        400: OpenApiResponse(
            description="Некорректный WKT или ошибка валидации.",
        ),
    },
    examples=[
        OpenApiExample(
            name="Пример запроса на создание геозоны",
            value={
                "name": "Склад №1",
                "geometry": WAREHOUSE_WKT,
            },
            request_only=True,
        ),
        OpenApiExample(
            name="Пример успешного ответа",
            value={
                "id": 1,
                "name": "Склад №1",
                "geometry": WAREHOUSE_WKT_RESPONSE,
            },
            response_only=True,
            status_codes=["201"],
        ),
    ],
)

geozone_list_schema = extend_schema(
    tags=["Geozones"],
    summary="Получить список геозон",
    description="Возвращает список всех геозон.",
    responses={
        200: OpenApiResponse(
            response=GeozoneSerializer(many=True),
            description="Список геозон.",
        ),
    },
    examples=[
        OpenApiExample(
            name="Пример ответа со списком геозон",
            value=[
                {
                    "id": 1,
                    "name": "Склад №1",
                    "geometry": WAREHOUSE_WKT_RESPONSE,
                },
                {
                    "id": 2,
                    "name": "Офис",
                    "geometry": OFFICE_WKT_RESPONSE,
                },
            ],
            response_only=True,
            status_codes=["200"],
        ),
    ],
)

check_create_schema = extend_schema(
    tags=["Checks"],
    summary="Проверить точку",
    description=(
        "Проверяет, попадает ли точка устройства в геозону, и сохраняет результат проверки."
    ),
    request=CheckPointInputSerializer,
    responses={
        201: OpenApiResponse(
            response=CheckSerializer,
            description="Результат проверки успешно сохранен.",
        ),
        400: OpenApiResponse(
            description="Ошибка валидации входных данных.",
        ),
    },
    examples=[
        OpenApiExample(
            name="Пример запроса на проверку точки",
            value={
                "device_id": "device-001",
                "lat": 55.7560,
                "lon": 37.6178,
            },
            request_only=True,
        ),
        OpenApiExample(
            name="Пример ответа: точка внутри геозоны",
            value={
                "id": 15,
                "device_id": "device-001",
                "lat": 55.7560,
                "lon": 37.6178,
                "inside": True,
                "matched_geozone": {
                    "id": 1,
                    "name": "Склад №1",
                },
                "created_at": "2026-03-30T12:00:00Z",
            },
            response_only=True,
            status_codes=["201"],
        ),
        OpenApiExample(
            name="Пример ответа: точка вне геозоны",
            value={
                "id": 16,
                "device_id": "device-002",
                "lat": 59.9391,
                "lon": 30.3158,
                "inside": False,
                "matched_geozone": None,
                "created_at": "2026-03-30T12:05:00Z",
            },
            response_only=True,
            status_codes=["201"],
        ),
    ],
)

check_list_schema = extend_schema(
    tags=["Checks"],
    summary="Получить список проверок",
    description="Возвращает список проверок с возможностью фильтрации.",
    parameters=[
        OpenApiParameter(
            name="device_id",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Фильтр по идентификатору устройства.",
        ),
        OpenApiParameter(
            name="inside",
            type=bool,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Фильтр по попаданию в геозону.",
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=CheckSerializer(many=True),
            description="Список проверок.",
        ),
    },
    examples=[
        OpenApiExample(
            name="Пример ответа со списком проверок",
            value=[
                {
                    "id": 15,
                    "device_id": "device-001",
                    "lat": 55.7560,
                    "lon": 37.6178,
                    "inside": True,
                    "matched_geozone": {
                        "id": 1,
                        "name": "Склад №1",
                    },
                    "created_at": "2026-03-30T12:00:00Z",
                },
                {
                    "id": 16,
                    "device_id": "device-002",
                    "lat": 59.9391,
                    "lon": 30.3158,
                    "inside": False,
                    "matched_geozone": None,
                    "created_at": "2026-03-30T12:05:00Z",
                },
            ],
            response_only=True,
            status_codes=["200"],
        ),
    ],
)

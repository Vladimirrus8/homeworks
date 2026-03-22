from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Sensor, Measurement
from .serializers import (
    SensorSerializer,
    SensorDetailSerializer,
    MeasurementCreateSerializer,
)


class SensorListCreateView(generics.ListCreateAPIView):
    """
    GET: возвращает список всех датчиков с базовой информацией.
    POST: создает новый датчик.
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    GET: возвращает полную информацию о датчике.
    PATCH/PUT: обновляет информацию о датчике.
    """
    queryset = Sensor.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SensorSerializer
        return SensorDetailSerializer


class MeasurementCreateView(generics.CreateAPIView):
    """
    POST: создает новое измерение для указанного датчика.
    Поддерживает загрузку изображений.
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementCreateSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sensor_id = serializer.validated_data['sensor'].id
        sensor = get_object_or_404(Sensor, id=sensor_id)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'status': 'success',
                'message': (
                    f'Измерение для датчика {sensor.name} '
                    f'успешно добавлено'
                ),
                'data': serializer.data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
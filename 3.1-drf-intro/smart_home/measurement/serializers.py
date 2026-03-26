from rest_framework import serializers
from .models import Sensor, Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    """
    Используется для создания и отображения измерений.
    """
    class Meta:
        model = Measurement
        fields = ['id', 'temperature', 'created_at', 'image']
        read_only_fields = ['id', 'created_at']


class SensorSerializer(serializers.ModelSerializer):
    """
    Используется для создания, обновления и отображения базовой информации.
    """
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class SensorDetailSerializer(serializers.ModelSerializer):
    """
    Включает все измерения, связанные с конкретным датчиком.
    """
    measurements = MeasurementSerializer(
        many=True,
        read_only=True,
        source='measurements.all'
    )

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']
        read_only_fields = ['id']


class MeasurementCreateSerializer(serializers.ModelSerializer):
    """
    Принимает ID датчика и температуру, опционально изображение.
    """
    class Meta:
        model = Measurement
        fields = ['sensor', 'temperature', 'image']

    def validate_temperature(self, value):
        if value < -100 or value > 100:
            raise serializers.ValidationError(
                'Температура должна быть в диапазоне от -100 до +100°C'
            )
        return value

    def validate_sensor(self, value):
        if not Sensor.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(
                'Датчик с указанным ID не найден'
            )
        return value
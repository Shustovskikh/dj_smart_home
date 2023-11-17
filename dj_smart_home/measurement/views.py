from django.shortcuts import render
from rest_framework import viewsets
from .models import Sensor, Measurement
from .serializers import SensorSerializer, MeasurementSerializer, SensorDetailSerializer

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SensorDetailSerializer
        return super().get_serializer_class()

class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

def sensor_view(request):
    sensors = Sensor.objects.all()
    measurements = Measurement.objects.filter(sensor__in=sensors)
    return render(request, 'measurement/sensors.html', {'sensors': sensors, 'measurements': measurements})
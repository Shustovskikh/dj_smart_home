from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Sensor, Measurement
from .serializers import SensorSerializer, MeasurementSerializer

class SensorTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sensor = Sensor.objects.create(name='Test Sensor', description='Test Description')
        self.measurement = Measurement.objects.create(sensor=self.sensor, temperature=22.5)

    def test_create_sensor(self):
        response = self.client.post(reverse('sensor-list'), {'name': 'New Sensor', 'description': 'New Description'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Sensor.objects.count(), 2)

    def test_update_sensor(self):
        response = self.client.patch(reverse('sensor-detail', args=[self.sensor.id]), {'description': 'Updated Description'})
        self.assertEqual(response.status_code, 200)
        self.sensor.refresh_from_db()
        self.assertEqual(self.sensor.description, 'Updated Description')

    def test_create_measurement(self):
        response = self.client.post(reverse('measurement-list'), {'sensor': self.sensor.id, 'temperature': 23.5})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Measurement.objects.count(), 2)

    def test_get_sensors(self):
        response = self.client.get(reverse('sensor-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_sensor_detail(self):
        response = self.client.get(reverse('sensor-detail', args=[self.sensor.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['measurements']), 1)
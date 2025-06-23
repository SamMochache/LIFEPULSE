from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User
from vitals.models import (
    SleepRecord, WeightRecord, HeartRateRecord,
    BloodPressureRecord, BloodSugarRecord
)


class BaseVitalsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass1234')
        self.other_user = User.objects.create_user(username='user2', password='pass1234')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


class SleepRecordTest(BaseVitalsTest):
    def test_create_sleep_record(self):
        url = reverse('sleep-list')
        data = {
            "date": "2025-06-23",
            "hours_slept": 7.5,
            "sleep_quality": "good"
        }
        response = self.client.post(url, data)
        print(response.status_code, response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SleepRecord.objects.count(), 1)

    def test_user_specific_sleep_data(self):
        SleepRecord.objects.create(user=self.user, date="2025-06-23", hours_slept=7, sleep_quality='good')
        SleepRecord.objects.create(user=self.other_user, date="2025-06-23", hours_slept=4, sleep_quality='poor')
        url = reverse('sleep-list')
        response = self.client.get(url)
        print(response.status_code, response.data)

        self.assertEqual(len(response.data), 1)  # Only user1's data visible


class WeightRecordTest(BaseVitalsTest):
    def test_create_weight_record(self):
        url = reverse('weight-list')
        data = {
            "date": "2025-06-23",
            "weight_kg": 68.5
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WeightRecord.objects.count(), 1)
        self.assertIn('bmi', response.data)

    def test_user_specific_weight_data(self):
        WeightRecord.objects.create(user=self.user, date="2025-06-23", weight_kg=70)
        WeightRecord.objects.create(user=self.other_user, date="2025-06-23", weight_kg=75)
        url = reverse('weight-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)


class HeartRateRecordTest(BaseVitalsTest):
    def test_create_hr_record(self):
        url = reverse('heartrate-list')
        data = {
            "date": "2025-06-23",
            "resting_hr": 60,
            "high_hr": 120,
            "low_hr": 55
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HeartRateRecord.objects.count(), 1)

    def test_user_specific_hr_data(self):
        HeartRateRecord.objects.create(user=self.user, date="2025-06-23", resting_hr=65, high_hr=130, low_hr=50)
        HeartRateRecord.objects.create(user=self.other_user, date="2025-06-23", resting_hr=70, high_hr=140, low_hr=55)
        url = reverse('heartrate-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)


class BloodPressureRecordTest(BaseVitalsTest):
    def test_create_bp_record(self):
        url = reverse('bloodpressure-list')
        data = {
            "date": "2025-06-23",
            "systolic": 122,
            "diastolic": 82,
            "pulse": 72
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BloodPressureRecord.objects.count(), 1)

    def test_user_specific_bp_data(self):
        BloodPressureRecord.objects.create(user=self.user, date="2025-06-23", systolic=120, diastolic=80, pulse=70)
        BloodPressureRecord.objects.create(user=self.other_user, date="2025-06-23", systolic=130, diastolic=85, pulse=75)
        url = reverse('bloodpressure-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)


class BloodSugarRecordTest(BaseVitalsTest):
    def test_create_sugar_record(self):
        url = reverse('bloodsugar-list')
        data = {
            "date": "2025-06-23",
            "fasting": 5.6,
            "post_meal": 7.8
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BloodSugarRecord.objects.count(), 1)

    def test_user_specific_sugar_data(self):
        BloodSugarRecord.objects.create(user=self.user, date="2025-06-23", fasting=5.5, post_meal=7.5)
        BloodSugarRecord.objects.create(user=self.other_user, date="2025-06-23", fasting=6.0, post_meal=8.0)
        url = reverse('bloodsugar-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)

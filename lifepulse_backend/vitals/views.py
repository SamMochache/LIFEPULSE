from rest_framework import viewsets, permissions
from .models import (
    Vitals, SleepRecord, WeightRecord,
    HeartRateRecord, BloodPressureRecord, BloodSugarRecord
)
from .serializers import (
    VitalsSerializer, SleepRecordSerializer, WeightRecordSerializer,
    HeartRateRecordSerializer, BloodPressureRecordSerializer, BloodSugarRecordSerializer
)


class VitalsViewSet(viewsets.ModelViewSet):
    queryset = Vitals.objects.all()
    serializer_class = VitalsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vitals.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SleepRecordViewSet(viewsets.ModelViewSet):
    queryset = Vitals.objects.all()
    serializer_class = SleepRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SleepRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WeightRecordViewSet(viewsets.ModelViewSet):
    queryset = Vitals.objects.all()
    serializer_class = WeightRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WeightRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HeartRateRecordViewSet(viewsets.ModelViewSet):
    queryset = Vitals.objects.all()
    serializer_class = HeartRateRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HeartRateRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BloodPressureRecordViewSet(viewsets.ModelViewSet):
    queryset = Vitals.objects.all()
    serializer_class = BloodPressureRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BloodPressureRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BloodSugarRecordViewSet(viewsets.ModelViewSet):
    queryset = Vitals.objects.all()
    serializer_class = BloodSugarRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BloodSugarRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

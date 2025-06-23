from rest_framework import viewsets, permissions
from .models import (
    BodyTemperatureRecord, SpO2Record, StepCountRecord, Vitals, SleepRecord, WeightRecord,
    HeartRateRecord, BloodPressureRecord, BloodSugarRecord,
)
from .serializers import (
    BodyTemperatureRecordSerializer, SpO2RecordSerializer, StepCountRecordSerializer, VitalsSerializer, SleepRecordSerializer, WeightRecordSerializer,
    HeartRateRecordSerializer, BloodPressureRecordSerializer, BloodSugarRecordSerializer, 
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
import csv
from django.http import HttpResponse

# Map vital names to their models and export fields
VITAL_MODELS = {
    "heart_rate": (HeartRateRecord, ["date", "bpm"]),
    "blood_pressure": (BloodPressureRecord, ["date", "systolic", "diastolic"]),
    "weight": (WeightRecord, ["date", "weight"]),
    "sleep": (SleepRecord, ["date", "hours_slept"]),
    "blood_sugar": (BloodSugarRecord, ["date", "blood_sugar"]),
    "steps": (StepCountRecord, ["date", "steps"]),
    "temperature": (BodyTemperatureRecord, ["date", "temperature"]),
    "spo2": (SpO2Record, ["date", "spo2"]),
}

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


class StepCountRecordViewSet(viewsets.ModelViewSet):
    serializer_class = StepCountRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StepCountRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SpO2RecordViewSet(viewsets.ModelViewSet):
    serializer_class = SpO2RecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SpO2Record.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BodyTemperatureRecordViewSet(viewsets.ModelViewSet):
    serializer_class = BodyTemperatureRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BodyTemperatureRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HealthTimelineView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        range_type = request.GET.get("range", "7d")  # e.g. 7d, 30d, 3m
        end_date = datetime.today().date()
        
        # Parse range
        if range_type.endswith("d"):
            days = int(range_type[:-1])
            start_date = end_date - timedelta(days=days)
        elif range_type.endswith("m"):
            months = int(range_type[:-1])
            start_date = end_date - timedelta(days=30 * months)
        else:
            return Response({"error": "Invalid range"}, status=400)

        # Collect data by day
        timeline = {}
        for day in range((end_date - start_date).days + 1):
            date = start_date + timedelta(days=day)
            timeline[date.isoformat()] = {
                "heart_rate": None,
                "bp_systolic": None,
                "bp_diastolic": None,
                "weight": None,
                "sleep_hours": None,
                "blood_sugar": None,
                "steps": None,
                "temperature": None,
                "spo2": None,
            }

        user = request.user

        def add_avg(model, field, target_field, extra_filter=None):
            qs = model.objects.filter(user=user, date__range=(start_date, end_date))
            if extra_filter:
                qs = qs.filter(**extra_filter)
            for record in qs:
                d = record.date.isoformat()
                if d in timeline and getattr(record, field) is not None:
                    timeline[d][target_field] = getattr(record, field)

        add_avg(HeartRateRecord, "bpm", "heart_rate")
        add_avg(BloodPressureRecord, "systolic", "bp_systolic")
        add_avg(BloodPressureRecord, "diastolic", "bp_diastolic")
        add_avg(WeightRecord, "weight", "weight")
        add_avg(SleepRecord, "hours_slept", "sleep_hours")
        add_avg(BloodSugarRecord, "blood_sugar", "blood_sugar")
        add_avg(Vitals, "steps", "steps")
        add_avg(Vitals, "body_temperature", "temperature")
        add_avg(Vitals, "spo2", "spo2")

        return Response(list(timeline.values()))


class ExportVitalCSVView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vital = request.GET.get("vital")
        range_type = request.GET.get("range", "30d")

        if vital not in VITAL_MODELS:
            return Response({"error": "Invalid or missing vital"}, status=400)

        model, fields = VITAL_MODELS[vital]
        user = request.user

        # Date range
        end_date = datetime.today().date()
        if range_type.endswith("d"):
            start_date = end_date - timedelta(days=int(range_type[:-1]))
        elif range_type.endswith("m"):
            start_date = end_date - timedelta(days=int(range_type[:-1]) * 30)
        else:
            return Response({"error": "Invalid range format"}, status=400)

        queryset = model.objects.filter(user=user, date__range=(start_date, end_date))

        # Create CSV response
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={vital}_export.csv"
        writer = csv.writer(response)
        writer.writerow(fields)

        for record in queryset:
            writer.writerow([getattr(record, field) for field in fields])

        return response
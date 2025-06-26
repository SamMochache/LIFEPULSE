from django.conf import settings
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse
from django.shortcuts import redirect

from datetime import datetime, timedelta
import csv

from .models import (
    Alert, BodyTemperatureRecord, SpO2Record, StepCountRecord, Vitals, SleepRecord, WeightRecord,
    HeartRateRecord, BloodPressureRecord, BloodSugarRecord,
)
from .serializers import (
    AlertSerializer, BodyTemperatureRecordSerializer, SpO2RecordSerializer, StepCountRecordSerializer, VitalsSerializer, SleepRecordSerializer, WeightRecordSerializer,
    HeartRateRecordSerializer, BloodPressureRecordSerializer, BloodSugarRecordSerializer,
)
from .utils import trigger_alert
from .tasks import send_verification_email_task
from .tokens import account_activation_token

# Thresholds and templates
THRESHOLDS = {
    "heart_rate": {"min": 50, "max": 100},
    "blood_pressure": {"systolic_max": 140, "diastolic_max": 90},
    "blood_sugar": {"min": 70, "max": 140},
    "temperature": {"min": 36.1, "max": 37.8},
    "spo2": {"min": 95},
}

MESSAGES = {
    "heart_rate": "Abnormal heart rate: {} bpm",
    "blood_pressure": "High blood pressure: {}/{} mmHg",
    "blood_sugar": "Abnormal blood sugar: {} mg/dL",
    "temperature": "Abnormal body temperature: {} °C",
    "spo2": "Low SpO2: {}%",
}

# Export map
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

# -------------------------
# Vital ViewSets
# -------------------------

class VitalsViewSet(viewsets.ModelViewSet):
    serializer_class = VitalsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vitals.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HeartRateRecordViewSet(viewsets.ModelViewSet):
    serializer_class = HeartRateRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HeartRateRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        trigger_alert(
            user=self.request.user,
            vital_type="heart_rate",
            value=instance.bpm,
            thresholds=THRESHOLDS["heart_rate"],
            message_template=MESSAGES["heart_rate"]
        )
        



class BloodPressureRecordViewSet(viewsets.ModelViewSet):
    serializer_class = BloodPressureRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BloodPressureRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        trigger_alert(
            user=self.request.user,
            vital_type="blood_pressure",
            value=(instance.systolic, instance.diastolic),
            thresholds=THRESHOLDS["blood_pressure"],
            message_template=MESSAGES["blood_pressure"]
        )
       



class BloodSugarRecordViewSet(viewsets.ModelViewSet):
    serializer_class = BloodSugarRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BloodSugarRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        trigger_alert(
            user=self.request.user,
            vital_type="blood_sugar",
            value=instance.blood_sugar,
            thresholds=THRESHOLDS["blood_sugar"],
            message_template=MESSAGES["blood_sugar"]
        )
        



class BodyTemperatureRecordViewSet(viewsets.ModelViewSet):
    serializer_class = BodyTemperatureRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BodyTemperatureRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        trigger_alert(
            user=self.request.user,
            vital_type="temperature",
            value=instance.temperature,
            thresholds=THRESHOLDS["temperature"],
            message_template=MESSAGES["temperature"]
        )
        



class SpO2RecordViewSet(viewsets.ModelViewSet):
    serializer_class = SpO2RecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SpO2Record.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        trigger_alert(
            user=self.request.user,
            vital_type="spo2",
            value=instance.spo2,
            thresholds=THRESHOLDS["spo2"],
            message_template=MESSAGES["spo2"]
        )



class WeightRecordViewSet(viewsets.ModelViewSet):
    serializer_class = WeightRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WeightRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SleepRecordViewSet(viewsets.ModelViewSet):
    serializer_class = SleepRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SleepRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StepCountRecordViewSet(viewsets.ModelViewSet):
    serializer_class = StepCountRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StepCountRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# -------------------------
# Timeline and Export
# -------------------------

class HealthTimelineView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        range_type = request.GET.get("range", "7d")
        end_date = datetime.today().date()

        if range_type.endswith("d"):
            days = int(range_type[:-1])
            start_date = end_date - timedelta(days=days)
        elif range_type.endswith("m"):
            months = int(range_type[:-1])
            start_date = end_date - timedelta(days=30 * months)
        else:
            return Response({"error": "Invalid range"}, status=400)

        timeline = {
            (start_date + timedelta(days=i)).isoformat(): {
                "heart_rate": None,
                "bp_systolic": None,
                "bp_diastolic": None,
                "weight": None,
                "sleep_hours": None,
                "blood_sugar": None,
                "steps": None,
                "temperature": None,
                "spo2": None,
            } for i in range((end_date - start_date).days + 1)
        }

        user = request.user

        def add_avg(model, field, target):
            for record in model.objects.filter(user=user, date__range=(start_date, end_date)):
                d = record.date.isoformat()
                if d in timeline:
                    timeline[d][target] = getattr(record, field, None)

        add_avg(HeartRateRecord, "resting_hr", "heart_rate")
        add_avg(BloodPressureRecord, "systolic", "bp_systolic")
        add_avg(BloodPressureRecord, "diastolic", "bp_diastolic")
        add_avg(WeightRecord, "weight_kg", "weight")
        add_avg(SleepRecord, "hours_slept", "sleep_hours")
        add_avg(BloodSugarRecord, "fasting", "blood_sugar")
        add_avg(StepCountRecord, "steps", "steps")
        add_avg(BodyTemperatureRecord, "temperature", "temperature")
        add_avg(SpO2Record, "spo2", "spo2")

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

        end_date = datetime.today().date()
        if range_type.endswith("d"):
            start_date = end_date - timedelta(days=int(range_type[:-1]))
        elif range_type.endswith("m"):
            start_date = end_date - timedelta(days=30 * int(range_type[:-1]))
        else:
            return Response({"error": "Invalid range format"}, status=400)

        queryset = model.objects.filter(user=user, date__range=(start_date, end_date))

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={vital}_export.csv"
        writer = csv.writer(response)
        writer.writerow(fields)
        for record in queryset:
            writer.writerow([getattr(record, field) for field in fields])

        return response

# -------------------------
# Alerts
# -------------------------

class AlertViewSet(viewsets.ModelViewSet):
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "user")

        if not all([username, email, password]):
            return Response({"detail": "All fields are required."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"detail": "Username already exists."}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"detail": "Email already exists."}, status=400)

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role=role,
            is_active=False  # disable account until email is verified
        )

        # Generate verification link
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        current_site = get_current_site(request).domain
        verify_url = f"http://{current_site}{reverse('activate-account', kwargs={'uidb64': uid, 'token': token})}"

        subject = "Verify your LifePulse Account"
        send_verification_email_task.delay(user.email, subject, verify_url)

        return Response(
            {"detail": "Registration successful. Check your email to verify your account."},
            status=status.HTTP_201_CREATED
        )


class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect(f"{settings.FRONTEND_URL}/login?activated=true")  # ✅ redirect to frontend login
        else:
            return Response({"detail": "Invalid or expired activation link."}, status=400)
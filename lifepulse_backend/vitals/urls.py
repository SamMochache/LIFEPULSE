from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    AlertViewSet,
    BodyTemperatureRecordViewSet,
    ExportVitalCSVView,
    SpO2RecordViewSet,
    StepCountRecordViewSet,
    VitalsViewSet,
    SleepRecordViewSet,
    WeightRecordViewSet,
    HeartRateRecordViewSet,
    BloodPressureRecordViewSet,
    BloodSugarRecordViewSet,
    HealthTimelineView,
    RegisterUserView,  # ✅ make sure to import this too 
     # ✅ make sure to import this too
)

router = DefaultRouter()
router.register(r'vitals', VitalsViewSet, basename='vitals')
router.register(r'sleep', SleepRecordViewSet, basename='sleep')
router.register(r'weight', WeightRecordViewSet, basename='weight')
router.register(r'heartrate', HeartRateRecordViewSet, basename='heartrate')
router.register(r'bloodpressure', BloodPressureRecordViewSet, basename='bloodpressure')
router.register(r'bloodsugar', BloodSugarRecordViewSet, basename='bloodsugar')
router.register(r'steps', StepCountRecordViewSet, basename='stepcountrecord')
router.register(r'spo2', SpO2RecordViewSet, basename='spo2record')
router.register(r'temperature', BodyTemperatureRecordViewSet, basename='bodytemperaturerecord')
router.register(r'alerts', AlertViewSet, basename='alerts')

# ✅ Append timeline path correctly
urlpatterns = router.urls + [
    path('timeline/', HealthTimelineView.as_view(), name='health-timeline'),
    path("export/", ExportVitalCSVView.as_view(), name="vital-export"),
    path("register/", RegisterUserView.as_view(), name="register"),
]

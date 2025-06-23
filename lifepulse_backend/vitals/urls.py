from rest_framework.routers import DefaultRouter
from .views import (
    BodyTemperatureRecordViewSet,
    SpO2RecordViewSet,
    StepCountRecordViewSet,
    VitalsViewSet,
    SleepRecordViewSet,
    WeightRecordViewSet,
    HeartRateRecordViewSet,
    BloodPressureRecordViewSet,
    BloodSugarRecordViewSet
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


urlpatterns = router.urls

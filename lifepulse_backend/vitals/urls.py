from rest_framework.routers import DefaultRouter
from .views import (
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

urlpatterns = router.urls

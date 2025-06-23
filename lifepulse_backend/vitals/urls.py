from rest_framework.routers import DefaultRouter
from .views import VitalsViewSet

router = DefaultRouter()
router.register(r'vitals', VitalsViewSet, basename='vitals')

urlpatterns = router.urls

from rest_framework import viewsets, permissions
from .models import Vitals
from .serializers import VitalsSerializer

class VitalsViewSet(viewsets.ModelViewSet):
    serializer_class = VitalsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vitals.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

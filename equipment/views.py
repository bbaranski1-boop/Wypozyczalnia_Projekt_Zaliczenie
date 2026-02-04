from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Equipment, CustomerProfile, Rental
from .serializers import CategorySerializer, EquipmentSerializer, CustomerProfileSerializer, RentalSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    permission_classes = [permissions.IsAdminUser | permissions.DjangoModelPermissionsOrAnonReadOnly]

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filterset_fields = ['category', 'is_available', 'size']
    search_fields = ['name', 'serial_number']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # --- ENDPOINT SPECJALNY 1: Raport Statystyk ---
    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_count = Equipment.objects.count()
        # Policz aktywne wypożyczenia (niewrócone)
        active_rentals_count = Rental.objects.filter(is_returned=False).count()
        # Oblicz dostępne
        available_count = total_count - active_rentals_count
        
        return Response({
            "total_equipment": total_count,
            "available_now": available_count,
            "currently_rented": active_rentals_count,
            "info": "Statystyki dynamiczne"
        })

class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAdminUser]

class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    filterset_fields = ['is_returned', 'customer']
    # Wypożyczać mogą tylko zalogowani użytkownicy
    permission_classes = [permissions.IsAuthenticated]

    # --- ENDPOINT SPECJALNY 2: Tylko aktywne wypożyczenia ---
    @action(detail=False, methods=['get'])
    def active(self, request):
        active_rentals = Rental.objects.filter(is_returned=False)
        serializer = self.get_serializer(active_rentals, many=True)
        return Response(serializer.data)
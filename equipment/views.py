from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Equipment, CustomerProfile, Rental
from .serializers import CategorySerializer, EquipmentSerializer, CustomerProfileSerializer, RentalSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filterset_fields = ['category', 'is_available', 'size']
    search_fields = ['name', 'serial_number']

    # --- ENDPOINT SPECJALNY 1: Raport Statystyk ---
    # Dostępny pod adresem: /api/equipment/stats/
    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_count = Equipment.objects.count()
        available_count = Equipment.objects.filter(is_available=True).count()
        rented_count = total_count - available_count
        
        return Response({
            "total_equipment": total_count,
            "available_now": available_count,
            "currently_rented": rented_count,
            "info": "Statystyki wygenerowane automatycznie"
        })

class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer

class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    filterset_fields = ['is_returned', 'customer']

    # --- ENDPOINT SPECJALNY 2: Tylko aktywne wypożyczenia ---
    # Dostępny pod adresem: /api/rentals/active/
    @action(detail=False, methods=['get'])
    def active(self, request):
        # Pobieramy tylko te, które nie zostały zwrócone (is_returned=False)
        active_rentals = Rental.objects.filter(is_returned=False)
        
        # Używamy tego samego serializera co zwykle, żeby dane wyglądały tak samo
        serializer = self.get_serializer(active_rentals, many=True)
        return Response(serializer.data)
from django.contrib import admin
from .models import Category, Equipment, CustomerProfile, Rental

# To sprawia, że modele są widoczne w panelu admina
# Dodajemy też konfigurację, jakie kolumny mają się wyświetlać

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_per_day', 'is_available')
    list_filter = ('category', 'is_available') # Boczny pasek do filtrowania
    search_fields = ('name', 'serial_number') # Pasek wyszukiwania

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'certification_level')

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('customer', 'start_date', 'end_date', 'is_returned')
    list_filter = ('is_returned', 'start_date')
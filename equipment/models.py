from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# 1. Kategoria sprzętu 
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nazwa kategorii")
    description = models.TextField(blank=True, verbose_name="Opis")

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def __str__(self):
        return self.name

# 2. Konkretny sprzęt
class Equipment(models.Model):
    # Lista dostępnych rozmiarów (wartość w bazie, nazwa wyświetlana)
    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('UNI', 'Uniwersalny'),
        ('10L', '10 Litrów'), # Np. dla butli
        ('12L', '12 Litrów'),
        ('15L', '15 Litrów'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='equipments')
    name = models.CharField(max_length=200, verbose_name="Nazwa sprzętu")
    # Numer seryjny odróżnia fizyczne sztuki od siebie!
    serial_number = models.CharField(max_length=100, unique=True, verbose_name="Numer seryjny")
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Cena za dobę (PLN)")
    
    # Tutaj dodaliśmy choices=SIZE_CHOICES
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, blank=True, verbose_name="Rozmiar/Pojemność")
    
    is_available = models.BooleanField(default=True, verbose_name="Dostępny")
    last_service_date = models.DateField(null=True, blank=True, verbose_name="Data ostatniego serwisu")

    class Meta:
        verbose_name = "Sprzęt"
        verbose_name_plural = "Sprzęt"

    def __str__(self):
        # Wyświetli się np.: "Pianka Scubapro (M) [SN: 12345]"
        return f"{self.name} ({self.size}) [SN: {self.serial_number}]"

# 3. Profil klienta (rozszerzenie standardowego Usera)
class CustomerProfile(models.Model):
    CERTIFICATES = [
        ('OWD', 'Open Water Diver'),
        ('AOWD', 'Advanced Open Water Diver'),
        ('RESCUE', 'Rescue Diver'),
        ('DM', 'Divemaster'),
        ('NONE', 'Brak certyfikatu'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, verbose_name="Numer telefonu")
    certification_level = models.CharField(max_length=10, choices=CERTIFICATES, default='NONE', verbose_name="Certyfikat")

    class Meta:
        verbose_name = "Profil klienta"
        verbose_name_plural = "Profile klientów"

    def __str__(self):
        return f"{self.user.username} - {self.get_certification_level_display()}"

# 4. Wypożyczenie
class Rental(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, verbose_name="Klient")
    equipment = models.ManyToManyField(Equipment, verbose_name="Wypożyczony sprzęt")
    start_date = models.DateField(default=timezone.now, verbose_name="Data wypożyczenia")
    end_date = models.DateField(verbose_name="Data zwrotu")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Koszt całkowity")
    is_returned = models.BooleanField(default=False, verbose_name="Zwrócono")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Wypożyczenie"
        verbose_name_plural = "Wypożyczenia"

    def save(self, *args, **kwargs):
        # Prosta logika: jeśli nie podano kosztu, policzymy go później (w widokach lub sygnałach)
        # Tutaj zostawiamy to puste, aby nie komplikować modeli na start
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Wypożyczenie {self.id} - {self.customer.user.username}"
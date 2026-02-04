from rest_framework import serializers
from .models import Category, Equipment, CustomerProfile, Rental

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class EquipmentSerializer(serializers.ModelSerializer):
  
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Equipment
        fields = '__all__'

class CustomerProfileSerializer(serializers.ModelSerializer):
  
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ['id', 'username', 'email', 'phone_number', 'certification_level']

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'
    
    
    def validate(self, data):
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError("Data zwrotu nie może być wcześniejsza niż data wypożyczenia!")
        return data
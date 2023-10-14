from rest_framework import serializers
from .models import BankCard, Transaction, Budget, Category
from django.contrib.auth.models import User
from django.utils import timezone

class BankCardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default =serializers.CurrentUserDefault())
    class Meta:
        model = BankCard
        fields = ('user','name', 'balance', 'initial_balance')
    def create(self, validated_data):
        balance = validated_data.pop('balance')
        bank_card = BankCard.objects.create(initial_balance=balance, **validated_data)
        return bank_card
        
class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default =serializers.CurrentUserDefault())
    class Meta:
        model = Category
        fields = ('name', 'user')

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default =serializers.CurrentUserDefault())
    date = serializers.HiddenField(default=timezone.now())
    category = serializers.CharField(default=None)
    class Meta:
        model = Transaction
        fields = ('amount', 'description', 'category','account', 'date', 'user', 'is_income')

class BudgetSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default =serializers.CurrentUserDefault())
    class Meta:
        model = Budget
        fields = ('user','limit', 'start_date', 'end_date', 'category')
        
class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'write-only': True}
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], password = validated_data['password']  ,first_name=validated_data['first_name'],  last_name=validated_data['last_name'])
        return user
    
# class IncomeSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     date = serializers.HiddenField(default=timezone.now())
#     class Meta:
#         model = Income
#         fields = ('user','account_balance','amount', 'date', 'description')
       
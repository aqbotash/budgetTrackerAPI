from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.utils import timezone
from .models import BankCard, Transaction, Budget, Category, Income, Expense
from .serializers import BankCardSerializer, TransactionSerializer,CategorySerializer,RegistrationSerializer, BudgetSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User


class CategoryAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class RegistrationAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    
class BankCardAPIView(generics.ListCreateAPIView):
    queryset = BankCard.objects.all()
    serializer_class = BankCardSerializer
    # authentication_classes = [JWTAuthentication]

class BankCardDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BankCard.objects.all()
    serializer_class = BankCardSerializer
      
class BudgetAPIView(generics.ListCreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    
class BudgetDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    
class FinancialReportAPIView(APIView):
    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        total_expense = 0
        bank_cards = BankCard.objects.all()
        total_income = sum(card.initial_balance for card in bank_cards)

        for transaction in transactions:
            if transaction.is_income:
                total_income+=transaction.amount
            else:
                total_expense+=transaction.amount
        net_income = total_income - total_expense
        message = "You are managing your budget well"
        if net_income < 0:
            message = "You are underbudget"
        return Response({"total_expense":total_expense, "total_income": total_income, "net_income": net_income, "message": message})
    
class TransactionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
class TransactionCreateAPIView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        transaction_data = serializer.validated_data
        transaction = Transaction.objects.create(
            user = self.request.user,
            account=transaction_data['account'],
            amount=transaction_data['amount'],
            category=transaction_data['category'],
            description = transaction_data['description'],
            is_income = transaction_data['is_income'],
            date = timezone.now())
        if transaction.is_income:
            transaction.account.balance += transaction.amount
            transaction.account.save()
            serializer.save()
        else:
            transaction.account.balance -= transaction.amount
            
            transaction.account.save()
            serializer.save()
            
    
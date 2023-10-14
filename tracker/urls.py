from django.urls import path, include
from . import views

name = 'tracker'

urlpatterns = [
    path('bank_card/', views.BankCardAPIView.as_view(), name='bank_card' ),
    path('bank_card/<int:pk>', views.BankCardDetailAPIView.as_view(), name='bank_card' ),
    path('budget/', views.BudgetAPIView.as_view(), name='post_budget' ),
    path('budget/<int:pk>', views.BudgetDetailAPIView.as_view(), name='category_detail' ),
    path('category/', views.CategoryAPIView.as_view(), name='post_category' ),
    path('category/<int:pk>', views.CategoryDetailAPIView.as_view(), name='budget_detail' ),
    path('finreport/', views.FinancialReportAPIView.as_view(), name='fin_report' ),
    path('registration/', views.RegistrationAPIView.as_view(), name='registration' ),
    path('transaction/', views.TransactionCreateAPIView.as_view(), name='transaction' ),
    path('transaction/<int:pk>', views.TransactionDetailAPIView.as_view(), name='transaction_detail' ),
]
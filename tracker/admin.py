from django.contrib import admin
from .models import Transaction, Budget, Category, BankCard

admin.site.register(Transaction)
admin.site.register(Budget)
admin.site.register(Category)
admin.site.register(BankCard)

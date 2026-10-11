from django.contrib import admin

# Register your models here.
from .models import Account, IncomeType, Income, ExpenseType, Expense

admin.site.register(Account)
admin.site.register(IncomeType)
admin.site.register(Income)
admin.site.register(ExpenseType)
admin.site.register(Expense)

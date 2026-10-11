from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
    ACCOUNT_TYPES = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank', 'Bank account'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounsts')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20,choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    currency = models.CharField(max_length=10,default='UZS')
   
    def __str__(self):
        return self.name

class IncomeType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='incomes')
    income_type = models.ForeignKey(IncomeType, on_delete=models.SET_NULL, null=True,blank=True,related_name='incomes')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    note = models.TextField(blank=True)

class ExpenseType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='expenses')
    expense_type = models.ForeignKey(ExpenseType, on_delete=models.SET_NULL, null=True,blank=True,related_name='expenses4')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    note = models.TextField(blank=True)

    def __str__(self):
        return str(self.amount)


    
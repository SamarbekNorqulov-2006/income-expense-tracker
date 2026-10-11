from rest_framework import serializers
from .models import Account, IncomeType, ExpenseType, Income,Expense

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id', 
            'user', 
            'name', 
            'type', 
            'balance', 
            'currency',
        ]
        read_only_fields = ['id', 'user',]

class IncomeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeType
        fields = ['id', 'name',]
        read_only_fields = ['id']

class ExpenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseType
        fields = ['id', 'name',]
        read_only_fields = ['id']

class IncomeSerializer(serializers.ModelSerializer):
    class Meta :
        model = Income
        fields = [
            'id',
            'user',
            'account',
            'income_type',
            'amount',
            'date',
            'note'
        ]
        read_only_fields = ['id', 'user']
    
    def validate_amount(self,value):
        if value <= 0:
            raise serializers.ValidationError(
            "Kirim 0 dan katta bo'lishi kerak")
        
        return value
    
    def validate(self, attrs):
        request = self.context.get('request')
        account = attrs.get('account', self.instance.account if self.instance else None)
        if request and  account and account.user !=request.user:
            raise serializers.ValidationError("Bu hisob sizga tegishli emas.")
        
        return attrs

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta :
        model = Expense
        fields = [
            'id',
            'user',
            'account',
            'expense_type',
            'amount',
            'date',
            'note'
        ]
        read_only_fields = ['id', 'user']

    def validate_amount(self,value):
        if value <= 0:
            raise serializers.ValidationError(
            "Chiqim 0 dan katta bo'lishi kerak")
        
        return value
    
    def validate(self, attrs):
        request = self.context.get('request')
        account = attrs.get('account', self.instance.account if self.instance else None)
        amount = attrs.get('amount', self.instance.amount if self.instance else None)
        if request and  account and account.user !=request.user:
            raise serializers.ValidationError("Bu hisob sizga tegishli emas.")
        
        if account and amount is not None:
            balance = account.balance

        if self.instance and self.instance.account_id == account.id:
            balance += self.instance.amount
            if amount > balance:
                raise serializers.ValidationError("Hisobda chiqim uchun mablag' yetarli emas.")
        
        return attrs
from django.shortcuts import render
from django.db import transaction
from django.db.models import F
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny

from .models import Account, Income, Expense, IncomeType, ExpenseType
from .serializers import (
    AccountSerializer,
    IncomeSerializer,
    ExpenseSerializer,
    IncomeTypeSerializer,
    ExpenseTypeSerializer
)

class AccountListCreateView(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)


class AccountListCreateView(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class IncomeListCreateView(generics.ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    @transaction.atomic
    def perform_create(self, serializer):
        income = serializer.save(user=self.request.user)

        Account.objects.filter(
            pk=income.account_id,
            user=self.request.user,
        ).update(balance=F('balance') + income.amount)

    @transaction.atomic
    def perform_update(self, serializer):
        old_income = self.get_object()
        old_account_id = old_income.account_id
        old_amount = old_income.amount

        income = serializer.save()

        Account.objects.filter(pk=old_account_id).update(
            balance=F('balance') - old_amount
        )
        Account.objects.filter(
            pk=income.account_id,
            user=self.request.user,
        ).update(balance=F('balance') + income.amount)

    @transaction.atomic
    def perform_destroy(self, instance):
        Account.objects.filter(pk=instance.account_id).update(
            balance=F('balance') - instance.amount
        )
        instance.delete()


class IncomeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    @transaction.atomic
    def perform_update(self, serializer):
        old_income = self.get_object()
        old_account_id = old_income.account_id
        old_amount = old_income.amount

        income = serializer.save()

        Account.objects.filter(pk=old_account_id).update(
            balance=F('balance') - old_amount
        )
        Account.objects.filter(
            pk=income.account_id,
            user=self.request.user,
        ).update(balance=F('balance') + income.amount)

    @transaction.atomic
    def perform_destroy(self, instance):
        Account.objects.filter(pk=instance.account_id).update(
            balance=F('balance') - instance.amount
        )
        instance.delete()


class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    @transaction.atomic
    def perform_create(self, serializer):
        expense = serializer.save(user=self.request.user)

        updated = Account.objects.filter(
            pk=expense.account_id,
            user=self.request.user,
            balance__gte=expense.amount,
        ).update(
            balance=F('balance') - expense.amount
        )

        if updated == 0:
            raise serializers.ValidationError(
                "Hisobda mablag' yetarli emas."
            )


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    @transaction.atomic
    def perform_update(self, serializer):
        old_expense = self.get_object()
        old_account_id = old_expense.account_id
        old_amount = old_expense.amount

        expense = serializer.save()

        Account.objects.filter(pk=old_account_id).update(
            balance=F('balance') + old_amount
        )
        Account.objects.filter(
            pk=expense.account_id,
            user=self.request.user,
        ).update(balance=F('balance') - expense.amount)

    @transaction.atomic
    def perform_destroy(self, instance):
        Account.objects.filter(pk=instance.account_id).update(
            balance=F('balance') + instance.amount
        )
        instance.delete()

class IncomeTypeListCreateView(generics.ListCreateAPIView):
    queryset = IncomeType.objects.all()
    serializer_class = IncomeTypeSerializer
    permission_classes = [IsAuthenticated]

class IncomeTypeDetailView(generics.RetrieveAPIView):
    queryset = IncomeType.objects.all()
    serializer_class = IncomeTypeSerializer
    permission_classes = [IsAuthenticated]

class ExpenseTypeListCreateView(generics.ListCreateAPIView):
    queryset = ExpenseType.objects.all()
    serializer_class = ExpenseTypeSerializer
    permission_classes = [IsAuthenticated]

class ExpenseTypeDetailView(generics.RetrieveAPIView):
    queryset = ExpenseType.objects.all()
    serializer_class = ExpenseTypeSerializer
    permission_classes = [IsAuthenticated]

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is None:
            return Response(
                {"error": "Login yoki parol noto‘g‘ri"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "username": user.username,
        })
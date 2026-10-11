from django.urls import path
from .views import (
    AccountListCreateView,
    AccountDetailView, 
    IncomeListCreateView, 
    IncomeDetailView, 
    ExpenseListCreateView, 
    ExpenseDetailView,
    IncomeTypeListCreateView,
    IncomeTypeDetailView,
    ExpenseTypeListCreateView,
    ExpenseTypeDetailView,
)
from .views import LoginAPIView

urlpatterns = [
    path('accounts/', AccountListCreateView.as_view(), name='account-list-create'),
    path('accounts/<int:pk>/', AccountDetailView.as_view(), name='account-detail'),
    path('incomes/', IncomeListCreateView.as_view(), name='income-list-create'),
    path('incomes/<int:pk>/', IncomeDetailView.as_view(), name='income-detail'),
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('expenses/<int:pk>/',ExpenseDetailView.as_view(), name='expense-detail'),
    path('income-types/', IncomeTypeListCreateView.as_view(),name='income-type-list'),
    path('income-types/<int:pk>/', IncomeTypeDetailView.as_view(),name='income-type-detail'),
    path('expense-types/', ExpenseTypeListCreateView.as_view(),name='expense-type-list'),
    path('expense-types/<int:pk>/', ExpenseTypeDetailView.as_view(),name='expense-type-detail'),
    path('login/', LoginAPIView.as_view(), name='login'),


]
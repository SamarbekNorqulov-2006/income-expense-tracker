Income Expense Tracker

Daromad va xarajatlarni boshqarish uchun Django REST Framework asosida yaratilgan loyiha.

Loyihaning imkoniyatlari

- Hisoblarni boshqarish (Accounts)
- Daromadlarni qo‘shish va ko‘rish (Incomes)
- Xarajatlarni qo‘shish va ko‘rish (Expenses)
- Daromad turlarini boshqarish (Income Types)
- Xarajat turlarini boshqarish (Expense Types)
- HTML, CSS va JavaScript orqali foydalanuvchi interfeysi

Texnologiyalar

- Python
- Django
- Django REST Framework
- HTML
- CSS
- JavaScript
- SQLite

Loyihani ishga tushirish

1. Repository’ni yuklab oling:
   
   git clone https://github.com/SamarbekNorqulov-2006/income-expense-tracker.git

2. Loyiha papkasiga kiring:
   
   cd income-expense-tracker

3. Virtual muhit yarating:
   
   python -m venv .venv

4. Virtual muhitni faollashtiring (Windows):
   
   .venv\Scripts\activate

5. Kerakli kutubxonalarni o‘rnating:
   
   pip install django djangorestframework drf-spectacular

6. Migratsiyalarni bajaring:
   
   python manage.py migrate

7. Serverni ishga tushiring:
   
   python manage.py runserver

8. Brauzerda oching:
   
   "http://127.0.0.1:8000/"

API endpointlari

Endpoint| Vazifasi
"/api/accounts/"| Hisoblar
"/api/incomes/"| Daromadlar
"/api/expenses/"| Xarajatlar
"/api/income-types/"| Daromad turlari
"/api/expense-types/"| Xarajat turlari

Muallif

Samarbek Norqulov

GitHub: https://github.com/SamarbekNorqulov-2006

GitHub (https://github.com/SamarbekNorqulov-2006/income-expense-tracker.git)
SamarbekNorqulov-2006/income-expense-tracker
Contribute to SamarbekNorqulov-2006/income-expense-tracker development by creating an account on GitHub.
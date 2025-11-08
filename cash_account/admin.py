from django.contrib import admin

from .models import CashAccount, Transaction, TransactionMethod


class TransactionMethodAdmin(admin.ModelAdmin):
    list_display = ["type", "created_at"]


class CashAccountAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "initial_balance",
        "current_balance",
        "is_active",
    ]


class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "type",
        "description",
        "cash_account",
        "transaction_method",
        "user",
        "amount",
        "transaction_date",
    ]


admin.site.register(CashAccount, CashAccountAdmin)
admin.site.register(TransactionMethod, TransactionMethodAdmin)
admin.site.register(Transaction, TransactionAdmin)

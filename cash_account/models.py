import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class TransactionMethod(models.Model):
    PAYMENT_TYPES = [
        ("cash", "Dinheiro"),
        ("pix", "Pix"),
        ("credit card", "Cartão de Crédito"),
    ]
    type = models.CharField("Tipo de pagamento", choices=PAYMENT_TYPES, unique=True)
    active = models.BooleanField("Ativo?", default=True)
    created_at = models.DateTimeField("Criado em:", auto_now_add=True)
    updated_at = models.DateTimeField("Modificado em:", auto_now=True)

    class Meta:
        verbose_name = "Método de pagamento"
        verbose_name_plural = "Métodos de pagamentos"
        ordering = ["created_at"]

    def __str__(self):
        return self.type


class CashAccount(models.Model):

    name = models.CharField("Nome", max_length=50, unique=True)
    description = models.TextField("Descrição", max_length=100, blank=True, null=True)
    initial_balance = models.DecimalField(
        "Saldo inicial", max_digits=12, decimal_places=2, default=0
    )
    current_balance = models.DecimalField(
        "Saldo atual", max_digits=12, decimal_places=2, blank=True, null=True
    )
    is_active = models.BooleanField("Ativo?", default=True)
    created_at = models.DateTimeField("Criado em:", auto_now_add=True)
    updated_at = models.DateTimeField("Modificado em:", auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.current_balance = self.initial_balance
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Conta"
        verbose_name_plural = "Contas"

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTION_TYPES = [("income", "Entrada"), ("expense", "Saída")]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField("Tipo de transação", choices=TRANSACTION_TYPES)
    description = models.TextField("Descrição", max_length=100, blank=True, null=True)
    cash_account = models.ForeignKey(
        CashAccount,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="Conta",
    )
    transaction_method = models.ForeignKey(
        TransactionMethod, on_delete=models.CASCADE, related_name="transactions"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    amount = models.DecimalField("Valor", max_digits=12, decimal_places=2)
    transaction_date = models.DateTimeField("Data da transação", auto_now_add=True)

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        ordering = ["-transaction_date"]

    def __str__(self):
        return f"{self.type} - {self.amount}"

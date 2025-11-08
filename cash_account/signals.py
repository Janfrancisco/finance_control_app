from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import CashAccount, Transaction


@receiver(pre_save, sender=Transaction)
def store_old_amount(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old = Transaction.objects.get(pk=instance.pk)
        except Transaction.DoesNotExist:
            instance._old = None

@receiver(post_save, sender=Transaction)
def update_value_on_save(sender, instance, created, **kwargs):
    account = instance.cash_account

    if created:
        value = instance.amount if instance.type == 'income' else -instance.amount
    else:
        old = instance._old
        value = 0
        value -= old.amount if old.type == 'expense' else -old.amount
        value += instance.amount if instance.type == 'expense' else -instance.amount

    account.current_balance += value
    account.save() 
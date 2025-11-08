from django.apps import AppConfig


class CashAccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cash_account"

    def ready(self):
        import cash_account.signals

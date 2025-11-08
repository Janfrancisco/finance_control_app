from django.urls import path

from .views import (TransactionCreateView, TransactionDetailView,
                    dashboard_view, export_transactions_to_pdf,
                    filter_transactions, list_transaction_view,
                    profile_settings_view, transaction_page)

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("statement/", list_transaction_view, name="statements"),
    path("statement/filter/", filter_transactions, name="filter_transactions"),
    path("details/<uuid:pk>", TransactionDetailView.as_view(), name="details"),
    path("profile/", profile_settings_view, name="profile_settings"),
    path("transactions/new", transaction_page, name="transaction_page"),
    path("transaction/create", TransactionCreateView.as_view(), name="add_new_transaction",
    ),
    path("transactions/pdf", export_transactions_to_pdf, name="export_to_pdf"),
]

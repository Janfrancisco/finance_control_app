from collections import defaultdict
from datetime import date
from decimal import Decimal

from babel.dates import format_date
from django.db.models import Avg, Sum
from django.utils.timezone import localtime, now

from cash_account.models import CashAccount, Transaction, TransactionMethod


def get_dashboard_data() -> dict:
    transactions = Transaction.objects.all()
    current_balance = CashAccount.objects.first().current_balance

    data = get_totals_data(transactions)

    pix_income = data.get("income", {}).get("pix", 0)
    pix_expense = data.get("expense", {}).get("pix", 0)

    cash_income = data.get("income", {}).get("cash", 0)
    cash_expense = data.get("expense", {}).get("cash", 0)

    total_income = cash_income + pix_income
    total_expense = cash_expense + pix_expense
    total_cash = cash_income - cash_expense
    total_pix = pix_income - pix_expense
    total = total_cash + total_pix
    percent_cash = (total_cash / total * 100) if total else 0
    percent_pix = (total_pix / total * 100) if total else 0
    money_saved = total_income - total_expense

    if total_income != 0:
        saving_rate = money_saved / total_income * 100
    else:
        saving_rate = 0

    if total_cash > total_pix:
        most_used_method = "Dinheiro"
    elif total_cash == total_pix:
        most_used_method = "Ambos"
    else:
        most_used_method = "Pix"

    difference = (
        total_cash - total_pix
        if most_used_method == "Dinheiro"
        else total_pix - total_cash
    )

    today = now().date()
    current_month_transactions = Transaction.objects.filter(
        transaction_date__year=today.year, transaction_date__month=today.month
    )
    total_month_income = current_month_transactions.filter(type="income").aggregate(
        total=Sum("amount")
    )["total"]
    total_month_expense = current_month_transactions.filter(type="expense").aggregate(
        total=Sum("amount")
    )["total"]
    income = total_month_income if total_month_income is not None else 0
    expense = total_month_expense if total_month_expense is not None else 0

    if expense != 0:
        monthly_trend = income / expense
    else:
        monthly_trend = 0

    context = {
        "cash_income": cash_income,
        "cash_expense": cash_expense,
        "pix_income": pix_income,
        "pix_expense": pix_expense,
        "current_balance": current_balance,
        "total_income": total_income,
        "total_expense": total_expense,
        "total_cash": total_cash,
        "total_pix": total_pix,
        "transactions": transactions,
        "recent_transactions": transactions[:5],
        "average_transactions": transactions.aggregate(avg=Avg("amount"))["avg"],
        "percent_cash": f"{percent_cash:.1f}",
        "percent_pix": f"{percent_pix:.1f}",
        "money_saved": money_saved,
        "saving_rate": f"{saving_rate:.1f}",
        "most_used_method": most_used_method,
        "difference": difference,
        "monthly_trend": f"{monthly_trend:.1f}",
    }

    return context


def get_statement_data(context: dict) -> dict:
    total_income = (
        context["transactions"]
        .filter(type="income")
        .aggregate(total=Sum("amount"))["total"]
        or 0
    )
    total_expense = (
        context["transactions"]
        .filter(type="expense")
        .aggregate(total=Sum("amount"))["total"]
        or 0
    )

    transanctions_method = TransactionMethod.objects.all().filter(active=True)

    types = dict(Transaction.TRANSACTION_TYPES)

    context["grouped_transactions"] = grouped_transactions(context["transactions"])
    context["total_income"] = total_income
    context["total_expense"] = total_expense
    context["transactions_method"] = transanctions_method
    context["types"] = types
    return context


def grouped_transactions(transactions):
    grouped = defaultdict(list)
    for tx in transactions:
        date_obj = localtime(tx.transaction_date).date()
        date_str = format_date(
            date_obj, format="EEEE, d 'de' MMMM 'de' yyyy", locale="pt_BR"
        )
        grouped[date_str.capitalize()] += [tx]
    return dict(grouped)


def get_totals_data(transactions: Transaction) -> dict:
    result = (
        transactions.all()
        .values("type", "transaction_method__type")
        .annotate(total_amount=Sum("amount"))
        .order_by("type", "transaction_method__type")
    )
    data = defaultdict(dict)

    for row in result:
        t_type = row["type"]
        pm_name = row["transaction_method__type"]
        total = row["total_amount"] or Decimal("0")
        data[t_type][pm_name] = total

    return data

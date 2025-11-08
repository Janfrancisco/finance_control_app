import json
from datetime import datetime

import weasyprint
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import (login_required,
                                            permission_required,
                                            user_passes_test)
from django.contrib.staticfiles import finders
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.timezone import localtime
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView

from app.services.transaction_service import (get_dashboard_data,
                                              get_statement_data,
                                              grouped_transactions)
from cash_account.forms import (AddNewTransactionForm,
                                CustomPasswordChangeForm, UserAvatarUpdateForm)

from .models import CashAccount, Transaction


@login_required
def dashboard_view(request):
    context = get_dashboard_data()

    return render(request, "dashboard.html", context)


@login_required
def list_transaction_view(request):
    transactions = Transaction.objects.all()
    context = get_statement_data({"transactions": transactions})

    return render(request, "statement.html", context)


@login_required
def get_filtered_transactions(request):
    transactions = Transaction.objects.all()
    context = dict()
    context["selected_type"] = request.GET.get("type", "")
    context["selected_method"] = request.GET.get("transaction_method", "")

    search = request.GET.get("search")
    tx_type = request.GET.get("type")
    transaction_method = request.GET.get("transaction_method")
    initial_date = request.GET.get("initial_date")
    end_date = request.GET.get("end_date")

    if search:
        transactions = transactions.filter(description__icontains=search)
    if tx_type:
        transactions = transactions.filter(type=tx_type)
    if transaction_method:
        transactions = transactions.filter(transaction_method__id=transaction_method)
    if initial_date:
        transactions = transactions.filter(transaction_date__gte=initial_date)
    if end_date:
        transactions = transactions.filter(transaction_date__date__lte=end_date)
    return transactions


@login_required
def filter_transactions(request):
    transactions = get_filtered_transactions(request)
    context = {
        "transactions": transactions,
        "grouped_transactions": grouped_transactions(transactions),
    }

    return render(request, "partials/_transaction_items.html", context)


@login_required
def profile_settings_view(request):
    if request.method == "POST":
        if "updateAvatar" in request.POST:
            user_form = UserAvatarUpdateForm(
                request.POST, request.FILES, instance=request.user
            )
            if user_form.is_valid():
                user_form.save()
                return redirect("profile_settings")
        elif "updatePassword" in request.POST:
            change_password_form = CustomPasswordChangeForm(
                user=request.user, data=request.POST
            )
            user_form = UserAvatarUpdateForm(instance=None)
            if change_password_form.is_valid():
                user = change_password_form.save()
                update_session_auth_hash(request, user)
                return redirect(reverse("profile_settings") + "?password_changed=true")
            else:
                messages.error(
                    request, "Erro ao alterar a senha. Verifique os dados informados."
                )
    else:
        change_password_form = CustomPasswordChangeForm(user=request.user)
        user_form = UserAvatarUpdateForm(instance=None)
    return render(
        request,
        "profile_settings.html",
        {"user_form": user_form, "change_password_form": change_password_form},
    )


@method_decorator(login_required, name="dispatch")
class TransactionDetailView(DetailView):
    model = Transaction
    template_name = "detail.html"
    context_object_name = "transaction"


@login_required
def transaction_page(request):
    form = AddNewTransactionForm()
    total_pix = get_dashboard_data()["total_pix"]
    total_cash = get_dashboard_data()["total_cash"]
    return render(
        request,
        "add_new_transaction.html",
        {"total_pix": total_pix, "total_cash": total_cash, "form": form},
    )


@method_decorator(login_required, name="dispatch")
class TransactionCreateView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        form = AddNewTransactionForm(data)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.cash_account = CashAccount.objects.first()
            transaction.user = request.user
            transaction.save()
            return JsonResponse({"sucess": True})
        return JsonResponse({"sucess": False, "errors": form.errors}, status=400)


@login_required
def export_transactions_to_pdf(request):
    transactions = get_filtered_transactions(request)
    date_of_issue = datetime.now()
    logo_path = finders.find("images/logo.png")
    context = {
        "transactions": transactions,
        "grouped_transactions": grouped_transactions(transactions),
        "date_of_issue": date_of_issue,
        "current_balance": get_dashboard_data()["current_balance"],
        "user": request.user.full_name,
    }

    html = render_to_string("pdf/extrato.html", context)
    pdf = weasyprint.HTML(string=html).write_pdf()
    content_disposition = ""
    # 2️⃣ Detect if mobile
    user_agent = request.META.get("HTTP_USER_AGENT", "").lower()
    is_mobile = any(m in user_agent for m in ["iphone", "android", "ipad", "mobile"])

    if is_mobile:
        content_disposition = 'attachment; filename="relatorio.pdf"'
    else:
        content_disposition = 'inline; filename="relatorio.pdf"'
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = content_disposition
    return response

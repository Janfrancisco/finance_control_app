from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from app.services.transaction_service import get_totals_data
from custom_user.models import CustomUser

from .models import CashAccount, Transaction


class UserAvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(
                attrs={
                    'class': 'hidden',
                    'accept': 'image/*',
                    'id': 'avatarInput'
                }
            )
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].required = False
        self.fields['new_password1'].required = False
        self.fields['new_password2'].required = False

        labels = {
            'old_password': 'Senha atual',
            'new_password1': 'Nova senha',
            'new_password2': 'Confirmar nova senha'
        }
        placeholders = {
            'old_password': 'Digite sua senha atual',
            'new_password1': 'Digite sua nova senha',
            'new_password2': 'Confirme sua nova senha'
        }
        for name, field in self.fields.items():
            label = labels.get(name, 'senha')
            placeholder = placeholders.get(name, 'Digite a senha')
            field.label = label
            field.widget.attrs.update({
                'class': 'w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': placeholder,
            })
        
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
    
        if not old_password or old_password.strip() == '':
            raise forms.ValidationError(
                'Por favor, digite sua senha atual. Este campo é obrigatório.',
                code='required'
            )
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                'A senha atual digitada está incorreta. Por favor, verifique e tente novamente.',
                code='password_incorrect'
            )
        
        return old_password
        return old_password
    
    def clean_new_password1(self):
        """Validação personalizada para nova senha"""
        new_password1 = self.cleaned_data.get('new_password1')
        
        if not new_password1 or new_password1.strip() == '':
            raise forms.ValidationError(
                'Por favor, digite uma nova senha. Este campo é obrigatório.',
                code='required'
            )
        
        return new_password1

    def clean_new_password2(self):
        """Validação personalizada para confirmação da nova senha"""
        new_password2 = self.cleaned_data.get('new_password2')
        
        if not new_password2 or new_password2.strip() == '':
            raise forms.ValidationError(
                'Por favor, confirme sua nova senha. Este campo é obrigatório.',
                code='required'
            )
        
        return new_password2

class AddNewTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'amount', 'transaction_method', 'description']

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.transactions = Transaction.objects.all()
            self.totals = get_totals_data(self.transactions)

 
    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data.get('type')
        amount = cleaned_data.get('amount')
        transaction_method = cleaned_data.get('transaction_method')


        if type == 'expense':
            pix_income = self.totals.get("income", {}).get("pix", 0)
            pix_expense = self.totals.get("expense", {}).get("pix", 0)

            cash_income = self.totals.get("income", {}).get("cash", 0)
            cash_expense = self.totals.get("expense", {}).get("cash", 0)
            total_cash = cash_income - cash_expense
            total_pix = pix_income - pix_expense

            if transaction_method.type == "pix" and amount > total_pix:
                self.add_error('amount', 'O valor desejado ultrapassa o valor disponível em pix.') 
            if transaction_method.type == "cash" and amount > total_cash:
                self.add_error('amount', 'O valor desejado ultrapassa o valor disponível em dinheiro.')
        return cleaned_data

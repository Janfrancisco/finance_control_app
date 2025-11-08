from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuário",
        required=True,
        widget=forms.TextInput(attrs={"autofocus": True}),
        error_messages={"required": "Por favor, preencha o campo de email."},
    )
    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput,
        error_messages={"required": "Por favor, preencha o campo de senha."},
    )

    # Overriding the clean method to customize invalid credentials error
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    _("Usuário ou senha incorretos."),
                    code="invalid_login",
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

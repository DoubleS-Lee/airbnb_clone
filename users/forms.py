from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # 이메일이나 비밀번호가 있는 field를 확인하고 싶으면 메소드명에 꼭 clean_을 붙여줘야한다
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))

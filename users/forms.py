from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirmă Parola")

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'birth_date','about_me','picture_profile')
        widgets = {
            'password': forms.PasswordInput(),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'about_me': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Parolele nu se potrivesc.")

        return cleaned_data

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'birth_date','about_me','picture_profile')  # Câmpurile pe care vrei să le afișezi/modifici
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'about_me': forms.Textarea(attrs={'rows': 3}),
        }
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Users

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ('email', 'first_name', 'last_name', 'birth_date')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Users
        fields = ('email', 'first_name', 'last_name', 'rating', 'is_active', 'is_staff', 'birth_date')
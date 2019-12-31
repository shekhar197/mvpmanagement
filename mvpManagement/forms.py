from django.forms import ModelForm
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import BusInfo, BusFare, DailyExpenses

class UserForm(ModelForm):
    class Meta:
        model=User
        fields=['usertype', 'first_name', 'last_name', 'username', 'email']

class BusInfoForm(ModelForm):
    class Meta:
        model=BusInfo
        fields='__all__'        

class BusFareForm(ModelForm):
    class Meta:
        model=BusFare
        fields='__all__'
    
class DailyExpensesForm(ModelForm):
    class Meta:
        model=DailyExpenses
        fields='__all__'
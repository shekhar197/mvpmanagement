from django.forms import ModelForm
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import BusInfo, BusInfoUser, BusFare, DailyExpenses

class UserForm(ModelForm):
    class Meta:
        model=User
        fields=['usertype', 'first_name', 'last_name', 'username', 'email']

class BusInfoForm(ModelForm):
    class Meta:
        model=BusInfo
        fields=['bnum', 'broute_from', 'broute_to', 'btrip', 'btriphrs','btotalfare','bseater']

class BusInfoUserForm(ModelForm):
    class Meta:
        model=BusInfoUser
        fields=['businfo','businfo_driver','businfo_condutor','businfo_helper'] 

    # def __init__(self, user, *args, **kwargs):
    #     super(BusInfoUserForm, self).__init__(*args, **kwargs)
    #     self.fields['businfo_driver'].queryset = User.objects.filter()
    #     self.fields['businfo_condutor'].queryset = User.objects.filter()
    #     self.fields['businfo_helper'].queryset = User.objects.filter()

class BusFareForm(ModelForm):
    class Meta:
        model=BusFare
        fields='__all__'
    
class DailyExpensesForm(ModelForm):
    class Meta:
        model=DailyExpenses
        fields='__all__'
from django import forms
from django.forms import ModelForm, ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import BusInfo, BusFare, DailyExpenses, BusSchedule
from django.contrib import messages

class DateInput(forms.DateInput):
    input_type = 'date'

class UserForm(ModelForm):
    # username = widget(username==unique)
    class Meta:
        model=User
        fields=['usertype', 'first_name', 'last_name', 'username', 'email']

    #def is_validate(self, instance)
    #def clean_data(self)
    def clean(self): 
        super(UserForm, self).clean() 
        username = self.cleaned_data.get('username') 
        email = self.cleaned_data.get('email')
        if len(username) < 5: 
            self._errors['username'] = self.error_class([ 
                'Minimum 5 characters required']) 
            messages.add_message(self, messages.INFO, "Minimum 5 characters required {0}".format(username))
        if len(email) <10: 
            self._errors['email'] = self.error_class([ 
                'Post Should Contain minimum 10 characters']) 
        return self.cleaned_data 

class BusInfoForm(ModelForm):
    class Meta:
        model=BusInfo
        fields=['bnum','bseater']

class BusScheduleForm(ModelForm):
    class Meta:
        model=BusSchedule
        fields=['businfo','broute_from','broute_to','btotalfare','businfo_driver','businfo_conductor','businfo_helper','bus_from','bus_to'] 
        widgets = {
            'bus_from': DateInput(),
            'bus_to': DateInput(),
        }

    def __init__(self, user, *args, **kwargs):
        super(BusScheduleForm, self).__init__(*args, **kwargs)
        self.fields['businfo_driver'].queryset = User.objects.filter(parent=user,usertype=2)
        self.fields['businfo_conductor'].queryset = User.objects.filter(parent=user,usertype=3)
        self.fields['businfo_helper'].queryset = User.objects.filter(parent=user,usertype=4)

# class BusInfoUserForm(ModelForm):
#     class Meta:
#         model=BusInfoUser
#         fields=['businfo','businfo_driver','businfo_condutor','businfo_helper'] 

    # def __init__(self, user, *args, **kwargs):
    #     super(BusInfoUserForm, self).__init__(*args, **kwargs)
    #     self.fields['businfo_driver'].queryset = User.objects.filter()
    #     self.fields['businfo_condutor'].queryset = User.objects.filter()
    #     self.fields['businfo_helper'].queryset = User.objects.filter()

class BusFareForm(ModelForm):
    class Meta:
        model=BusFare
        fields=['fare_bus','fare_origin','fare_destination','busfare','seatno','fare_date']
        widgets = {
            'fare_date': DateInput(),
        }

    def __init__(self, bus_detail, *args, **kwargs):
        super(BusFareForm, self).__init__(*args, **kwargs)
        self.fields['fare_bus'].queryset = BusScheduleForm.objects.filter(pk=bus_detail)
    
class DailyExpensesForm(ModelForm):
    class Meta:
        model=DailyExpenses
        fields='__all__'
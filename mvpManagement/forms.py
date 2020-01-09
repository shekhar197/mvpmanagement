import re
from datetime import date
from django import forms
from django.forms import ModelForm, ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import BusInfo, BusFare, DailyExpenses, BusSchedule
from django.contrib import messages


class DateInput(forms.DateInput):
    input_type = "date"


class UserForm(ModelForm):
    # username = widget(username==unique)
    class Meta:
        model = User
        fields = ["usertype", "first_name", "last_name", "username", "email"]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True

    # def is_validate(self, instance)
    # def clean_data(self)
    def clean(self):
        super(UserForm, self).clean()
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        username = self.cleaned_data.get("username")
        if bool(re.search(r'\d', first_name)):
            self._errors["first_name"] = self.error_class(
                ["First name should be characters."]
            )
        if bool(re.search(r'\d', last_name)):
            self._errors["last_name"] = self.error_class(
                ["Last name should be characters."]
            )
        if len(username) < 5:
            self._errors["username"] = self.error_class(
                ["Minimum 5 characters required"]
            )
        return self.cleaned_data


class BusInfoForm(ModelForm):
    class Meta:
        model = BusInfo
        fields = ["bnum", "bseater"]
    
    def clean(self):
        super(BusInfoForm, self).clean()
        bus_number = self.cleaned_data.get("bnum")
        bus_seater = self.cleaned_data.get("bseater")
        if len(bus_number) > 10:
            self._errors["bnum"] = self.error_class(
                ["Bus number should not be greater then 10 digits."]
            )
        if not bool(isinstance(bus_seater,int)):
            self._errors["bseater"] = self.error_class(
                ["Please use numeric fields."]
            )
        return self.cleaned_data

class BusScheduleForm(ModelForm):
    class Meta:
        model = BusSchedule
        fields = [
            "businfo",
            "broute_from",
            "broute_to",
            "btotalfare",
            "totaltrip",
            "businfo_driver",
            "businfo_conductor",
            "businfo_helper",
            "bus_from",
            "bus_to",
        ]
        widgets = {
            "bus_from": DateInput(),
            "bus_to": DateInput(),
        }

    def __init__(self, user, *args, **kwargs):
        super(BusScheduleForm, self).__init__(*args, **kwargs)
        self.fields["businfo_driver"].queryset = User.objects.filter(
            created_by=user, usertype=2
        )
        self.fields["businfo_conductor"].queryset = User.objects.filter(
            created_by=user, usertype=3
        )
        self.fields["businfo_helper"].queryset = User.objects.filter(
            created_by=user, usertype=4
        )
    
    def clean(self):
        super(BusScheduleForm, self).clean()
        bus_from = self.cleaned_data.get("bus_from")
        bus_to = self.cleaned_data.get("bus_to")
        total_trip = self.cleaned_data.get("totaltrip")
        today_date = date.today()
        if bus_from<today_date:
            self._errors["bus_from"] = self.error_class(
                ["You can not use past date."]
            )
        elif bus_from>bus_to:
            self._errors["bus_from"] = self.error_class(
                ["Your bus date from should be less then bus date to."]
            )
        if bus_to<today_date:
            self._errors["bus_to"] = self.error_class(
                ["You can not use past date."]
            )
        elif bus_to<bus_from:
            self._errors["bus_to"] = self.error_class(
                ["Your bus date to should be less then bus date from."]
            )
        if int(total_trip) == 0:
            self._errors["totaltrip"] = self.error_class(
                ["please input at least one trip."]
            )
        elif int(total_trip)>8:
            self._errors["totaltrip"] = self.error_class(
                ["Maximum 8 trip allow in a day."]
            )
        return self.cleaned_data



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
        model = BusFare
        fields = [
            "bus_info",
            "fare_origin",
            "fare_destination",
            "bus_fare",
            "seat_no",
            "trip",
            "fare_date",
        ]
        widgets = {
            "fare_date": DateInput(),
        }

    def __init__(self, bus_id, *args, **kwargs):
        super(BusFareForm, self).__init__(*args, **kwargs)
        self.fields["bus_info"].queryset = BusSchedule.objects.filter(pk=bus_id)

    
    def clean(self):
        super(BusFareForm, self).clean()
        fare_date = self.cleaned_data.get("fare_date")
        trip = self.cleaned_data.get("trip")
        today_date = date.today()
        if fare_date<today_date:
            self._errors["fare_date"] = self.error_class(
                ["Please Use current Date."]
            )
        elif fare_date>today_date:
            self._errors["fare_date"] = self.error_class(
                ["Please Use current Date."]
            )
        if trip==0:
            self._errors["trip"] = self.error_class(
                ["Please use correct trip."]
            )
        elif trip>4:
            self._errors["trip"] = self.error_class(
                ["Maximum 4 trip allow in a day."]
            )
        return self.cleaned_data


class DailyExpensesForm(ModelForm):
    class Meta:
        model = DailyExpenses
        fields = "__all__"

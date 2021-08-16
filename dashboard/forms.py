from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm


class NotesForm(forms.ModelForm):
    
    class Meta:
        model =Notes 
        fields = ("title","description")

#form for homeworks
class DateInput(forms.DateInput):
    input_type='date'
class HomeworkForm(forms.ModelForm):
    class Meta:
        model=Homework
        widgets={'due':DateInput()}
        fields=("title","subject","description","due","is_finished")


#form for youtube
class DashboardFom(forms.Form):
    text = forms.CharField(label="ENTER YOUR SEARCH: ", max_length=100)
class BookForm(forms.Form):
    strings= forms.CharField(label="Enter your book name:", max_length=100)


class TodoForm(forms.ModelForm):
    class Meta:
        model=TOdo
        fields=["title","is_finished"]


#form for the conversion
class ConverstionForm(forms.Form):
   CHOICES=[('length','Length'),('mass','Mass')]
   measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
class ConverstionLengthForm(forms.Form):
    CHOICES=[('yard','Yard'),('foot','Foot')]
    input = forms.CharField(label=False,widget=forms.TextInput(
        attrs ={'type':'number','placeholder':'Enter the Number'}
    ))
    measure1 = forms.CharField(
        label = '',
        widget=forms.Select(choices = CHOICES)
    )
    measure2 = forms.CharField(
        label = '',
        widget=forms.Select(choices = CHOICES)
    )
class ConverstionMassForm(forms.Form):
    CHOICES=[('pound','Pound'),('kilogram','Kilogram')]
    input = forms.CharField( required=False,label=False,widget=forms.TextInput(
        attrs ={'type':'number','placeholder':'Enter the Number'}
    ))
    measure1 = forms.CharField(
        label = '',widget=forms.Select(choices = CHOICES)
    )
    measure2 = forms.CharField(
        label = '',widget=forms.Select(choices = CHOICES)
    )

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']
    

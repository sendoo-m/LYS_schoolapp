from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }


class Student_edit_Form(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'national_number', 'gender', 'age', 'date_of_birth', 'academic_year', 'classroom']

# class StudentSearchForm(forms.Form):
#     search_query = forms.CharField(label='Search', required=False, max_length=100, 
#                                    widget=forms.TextInput(attrs={
#         'placeholder': 'Search by Name, National Number',
#         'class': 'form-control',
#     }))

# class StudentSearchForm(forms.Form):
#     search_query = forms.CharField(label='Search', required=False, max_length=100, 
#                                    widget=forms.TextInput(attrs={
#         'placeholder': 'Search by Name, National Number',
#         'class': 'form-control',
#     }))
#     educational_stage = forms.ModelChoiceField(queryset=EducationalStage.objects.all(), label='Educational Stage', required=False)
#     gender = forms.ChoiceField(choices=Student.GENDER_CHOICES, label='Gender', required=False)
#     # date_of_birth = forms.DateField(label='Date of Birth', required=False)
#     classroom = forms.ModelChoiceField(queryset=Classroom.objects.all(), label='Classroom', required=False)

from django import forms
from .models import Student, EducationalStage, Classroom

class StudentSearchForm(forms.Form):
    search_query = forms.CharField(
        label='Search', 
        required=False, 
        max_length=100, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by Name, National Number',
            'class': 'form-control',
        })
    )
    educational_stage = forms.ModelChoiceField(
        queryset=EducationalStage.objects.all(), 
        label='Educational Stage', 
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    gender = forms.ChoiceField(
        choices=Student.GENDER_CHOICES, 
        label='Gender', 
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    date_of_birth = forms.DateField(
        label='Date of Birth', 
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'form-control',
        })
    )
    classroom = forms.ModelChoiceField(
        queryset=Classroom.objects.all(), 
        label='Classroom', 
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['expense_type', 'amount', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

# class TuitionForm(forms.ModelForm):
#     class Meta:
#         model = Tuition
#         fields = ['installment_number', 'amount_tuition']



class TuitionForm(forms.ModelForm):
    class Meta:
        model = Tuition
        fields = ['installment_number', 'amount_tuition']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['receipt_date'].disabled = True



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'content']

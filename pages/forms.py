from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
from .models import RecordTransaction, FinancialGoal

class PasswordChangingForm(PasswordChangeForm):

    class Meta:
        model = User
        fields = ['old_password','new_password1', 'new_password2']

class SignUpForm(UserCreationForm):
    username = forms.CharField(label="",max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))

    class Meta:
        model = User
        fields = ['username','email']
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = 'Username'
        self.fields['username'].help_text = '<span class="form-text text-muted"><small></small></span>'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'User Name'
        self.fields['email'].label = 'Email'
        self.fields['email'].help_text = '<span class="form-text text-muted"><small></small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = 'Change Password'
        self.fields['password1'].help_text = '<span class="form-text text-muted small"></span>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small> </small></span>'


class ProfilePicForm(forms.ModelForm):
    image = forms.ImageField(label="Profile Picture")
    
    class Meta:
        model = Profile
        fields = ('image',)
       

class RecordTransactionForm(forms.ModelForm):
    class Meta:
        model = RecordTransaction
        fields = '__all__'

class FinancialGoalForm(forms.ModelForm):
    class Meta:
        model = FinancialGoal
        fields = ['name', 'goal_type', 'target_amount', 'deadline']
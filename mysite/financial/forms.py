from django import forms
from . import models

class UserAccountForm(forms.ModelForm):
  class Meta:
    model = models.UserAccount
    fields = ['name', 'interest_manage_rate', 'pick_up_rate', 'comment']

class RecordForm(forms.ModelForm):
  class Meta:
    model = models.AccountRecord
    fields = ['date', 'money']

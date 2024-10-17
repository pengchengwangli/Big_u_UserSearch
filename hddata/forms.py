# forms.py

from django import forms
from .models import Organization, Major

class UserProfileSearchForm(forms.Form):
    org_id = forms.ModelChoiceField(queryset=Organization.objects.all(), label='Organization (College)', required=True)
    major_id = forms.ModelChoiceField(queryset=Major.objects.none(), label='Major', required=False)


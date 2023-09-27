from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

from leads.models import Lead, Agent, Category, FollowUp

User = get_user_model()


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
            'description',
            'phone_number',
            'email',
            'profile_picture',
        )

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        return data


class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
        field_classes = {'username': UsernameField}


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        agents = Agent.objects.filter(organization=request.user.userprofile)
        super().__init__(*args, **kwargs)
        self.fields['agent'].queryset = agents


class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('category',)


class CategoryModelForm(forms.Form):
    class Meta:
        model = Category
        fields = ('name',)


class FollowUpModelForm(forms.Form):
    class Meta:
        model = FollowUp
        fields = ('notes', 'file', )

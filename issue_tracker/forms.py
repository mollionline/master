from django import forms

from issue_tracker.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['summary', 'description', 'status', 'type']


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False)

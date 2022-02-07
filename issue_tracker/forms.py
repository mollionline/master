from django import forms

from issue_tracker.models import Task, Project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['summary', 'description', 'status', 'type']


class SearchForm(forms.Form):
    search = forms.CharField(max_length=60, required=False)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project', 'description', 'created_at', 'updated_at']

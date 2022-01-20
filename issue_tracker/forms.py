from django import forms

from issue_tracker.models import Task, Status, Type


class TaskForm(forms.Form):
    summary = forms.CharField(max_length=50, required=True)
    description = forms.CharField(max_length=1000, required=False)
    status = forms.ModelChoiceField(queryset=Status.objects.all())
    type = forms.ModelChoiceField(queryset=Type.objects.all())

    def send_email(self):
        pass

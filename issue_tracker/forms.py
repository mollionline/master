from django import forms

from issue_tracker.models import Task, Status, Type


class TaskForm(forms.ModelForm):
    summary = forms.CharField(max_length=50, required=True)
    description = forms.CharField(max_length=1000, required=False)
    status = forms.ModelChoiceField(queryset=Status.objects.all())
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Task
        fields = '__all__'


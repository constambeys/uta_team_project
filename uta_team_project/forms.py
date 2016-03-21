from django import forms
from django.core.exceptions import ValidationError
from uta_models.models import *
from datetimewidget.widgets import DateTimeWidget


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('course', 'name')


class GroupForm(forms.ModelForm):
    def __init__(self, students_qs, limit, data=None):
        super(forms.ModelForm, self).__init__(data)
        self.fields['students'].queryset = students_qs
        self.limit = limit

    def clean_students(self):
        students = self.cleaned_data['students']
        if students.count() > self.limit:
            raise ValidationError("Maximum number allowed is " + str(self.limit))
        return students

    class Meta:
        model = Group
        fields = ('name', 'students')


class RequirementsForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = ('min_group_size', 'max_group_size')


class CourseAssignmentForm(forms.Form):
    course_assignment = forms.ModelChoiceField(queryset=Assignment.objects.all().order_by('name'))


class RatedQualificationForm(forms.Form):
    rated_qualifications = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'e.g. <Skill> <1-4>'}))


# https://github.com/asaglimbeni/django-datetime-widget
class DateTimeFieldForm(forms.Form):
    deadline = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=2))




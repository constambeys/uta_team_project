from django import forms
from django.core.exceptions import ValidationError
from uta_models.models import *


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('name', 'instructor', 'course', 'requirements', 'deadline')


class GroupForm(forms.ModelForm):
    def __init__(self, students, limit, data=None):
        super(forms.ModelForm, self).__init__(data)
        self.fields['students'].queryset = students
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
        fields = ('rated_qualifications', 'min_group_size', 'max_group_size')


class CourseAssignmentForm(forms.Form):
    course_assignment = forms.ModelChoiceField(queryset=Assignment.objects.all().order_by('name'))

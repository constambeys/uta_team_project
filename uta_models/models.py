from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify


# e.g Computing Science, Data Science
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return "Department: " + self.name


# e.g MSc, 4th year
class LevelOfStudy(models.Model):
    lvl = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return "Level Of Study: " + self.lvl


# e.g Internet Technology, Cyber Security
class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return "Course: " + self.name


class Qualification(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class RatedQualification(models.Model):
    qualification = models.ForeignKey(Qualification)
    rating = models.IntegerField(default=1, validators=[
            MaxValueValidator(4),
            MinValueValidator(1)
        ])

    def __unicode__(self):
        return "RatedQualification: " + self.qualification.name + " " + str(self.rating)


class Requirement(models.Model):
    min_group_size = models.IntegerField(default=1)
    max_group_size = models.IntegerField(default=2)
    rated_qualifications = models.ManyToManyField(RatedQualification)

    def __unicode__(self):
        return "Requirement: min group size " + str(self.min_group_size) + ", max group size " + str(
            self.max_group_size)
        + ", " + self.rated_qualifications


class Instructor(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return "Instructor: " + self.user.username


class Student(models.Model):
    user = models.OneToOneField(User)
    matriculationNumber = models.IntegerField(unique=True)
    department = models.ForeignKey(Department)
    lvlOfStudy = models.ForeignKey(LevelOfStudy)
    rated_qualifications = models.ManyToManyField(RatedQualification)

    def __unicode__(self):
        return "Student: " + self.user.username


class Assignment(models.Model):
    name = models.CharField(max_length=100, unique=True, default="Assignment")
    instructor = models.ForeignKey(Instructor)
    course = models.ForeignKey(Course)
    requirements = models.ForeignKey(Requirement)
    students = models.ManyToManyField(Student)
    deadline = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return "Assignment: " + self.name


class Group(models.Model):
    name = models.CharField(max_length=100, default="Group")
    assignment = models.ForeignKey(Assignment)
    students = models.ManyToManyField(Student)

    def __unicode__(self):
        return "Group: " + self.name
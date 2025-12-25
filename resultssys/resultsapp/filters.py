# from cgitb import lookup
from dataclasses import fields
from pyexpat import model
import django_filters
from django_filters import CharFilter,DateFilter
from .models import * 

# school filter
class School_filter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = School
        fields = ['name']


# student filter
class Student_filter(django_filters.FilterSet):
    index_number = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['index_number']
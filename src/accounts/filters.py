import django_filters
from django_filters import DateFilter
from .models import *
from django.forms.widgets import TextInput

class OrderFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name='date_created', lookup_expr='gte', label= 'After Date', widget=TextInput(attrs={'placeholder': 'mm/dd/yy'}))
	end_date = DateFilter(field_name='date_created', lookup_expr='lte', label = 'Before Date', widget=TextInput(attrs={'placeholder': 'mm/dd/yy'}))

	class Meta:
		model = Order
		fields = '__all__'
		exclude = ['customer', 'date_created']
		

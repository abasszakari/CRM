from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only


# Create your views here.
@unauthenticated_user
def register(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'Account was successfully created for ' + username)
			return redirect('accounts:login')
	context = {
		'form': form
	}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('accounts:home')
		else:
			messages.info(request, 'Username or Password is incorrect')
			return render(request, 'accounts/login.html')

	return render(request, 'accounts/login.html')

@login_required(login_url='accounts:login')
def logoutUser(request):
	logout(request)
	return redirect('accounts:login')

@login_required(login_url='accounts:login')
@admin_only
def home(request):
	customers = Customer.objects.all()
	orders = Order.objects.all()
	paginator = Paginator(orders, 5)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	total_customers = customers.count()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	context = {
		'customers': customers,
		'orders': orders,
		'total_customers': total_customers,
		'total_orders': total_orders,
		'delivered': delivered,
		'pending': pending,
		'page_obj':page_obj
	}

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	context = {
		'orders':orders,
		'total_orders': total_orders,
		'delivered': delivered,
		'pending': pending
	}

	return render(request, 'accounts/user.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)
	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()
	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()
	paginator = Paginator(products, 5)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {
		'page_obj': page_obj
	}
	return render(request, 'accounts/products.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()
	order_count = orders.count()
	
	my_filter = OrderFilter(request.GET, queryset=orders)
	orders = my_filter.qs

	context = {
		'customer':customer,
		'orders': orders,
		'order_count': order_count,
		'my_filter':my_filter
	}
	return render(request, 'accounts/customer.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
	customer = Customer.objects.get(id=pk)
	form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('accounts:home')
	context = {'form': form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('accounts:home')
	context = {'form': form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
	order = Order.objects.get(id=pk)
	customer = order.customer

	if request.method == 'POST':
		order.delete()
		return redirect('accounts:home')
	
	context = {
		'order': order,
		'customer': customer
	}
	return render(request, 'accounts/delete_order.html', context)


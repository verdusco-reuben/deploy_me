from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Poke
# Create your views here.
def logout(request):
	request.session.flush()
	return redirect('/')
def home(request):
	context = User.objects.homepage(request.session['id'])
	return render(request, 'test_app/home.html', context)
def poke(request, id):
	User.objects.total(id)
	Poke.objects.poke(request.session['id'], id)
	return redirect('/pokes')
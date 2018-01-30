from django.shortcuts import render, redirect
from django.db.models import permalink
from ..test_app.models import User, Poke
# Create your views here.
def index(request):
	return redirect('/main')
def main(request):
	return render(request, 'main_app/main.html')
def register(request):
	if request.path == '/login':
		result = User.objects.login(request.POST['email'],request.POST['password'])
	else:
		result = User.objects.register(request.POST['name'],request.POST['alias'],request.POST['password'], request.POST['password_confirm'],request.POST['email'],request.POST['dob'])
	if result[0]==True:
		request.session['name'] = result[1].alias
		request.session['id'] = result[1].id 
		return redirect('/pokes')
	else:
		request.session['errors'] = result[1]
		return redirect('/')
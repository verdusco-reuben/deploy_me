from __future__ import unicode_literals
from django.db import models
import re,bcrypt

# emailRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
	def register(self, name, alias, password, confirm_password, email, dob):
		errors = []
		if (len(name) == 0) or (len(alias) == 0) or (len(password) == 0):
			errors.append("Cannot be blank")
		elif (len(name) < 3) or (len(alias) < 3) or (len(password) < 8):
			errors.append("Input is too short")
		elif (not (password == confirm_password)):
			errors.append("Password don't match")
		# elif not emailRegex.match(email):
		# 	errors.append("Invalid email input")
		elif len(User.objects.filter(email=email)) > 0:
			errors.append("Email already taken")
		if len(errors) is not 0:
			return (False, errors)
		else:
			new_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			new_user = User.objects.create(name=name, alias=alias, password=new_pw, email=email, dob=dob)
			return (True, new_user)
	def login(self, email, password):
		# print "could it be?"
		errors = []
		try:
			b = User.objects.get(email=email)
			if bcrypt.checkpw(password.encode(), (b.password).encode()) == True:
				return (True, b)
			else:
				errors.append("Username/Password is invalid")
				return (False, errors)
		except:
			errors.append("Username/Password is invalid")
			return (False, errors)
	def homepage(self, id):
		context = {
			'user' : User.objects.get(id=id),
			'others' : User.objects.exclude(id=id).order_by('alias'),
			'pokes' : Poke.objects.filter(getting_poked=id).order_by('-single_poke_count'),
			'first' : User.objects.order_by('poke_history').last(),
			'last' : User.objects.order_by('poke_history').first(),
		}
		return context
	def total(self, id):
		user = User.objects.get(id=id)
		user.poke_history += 1
		user.save()

class PokeManager(models.Manager):
	def poke(self, is_poking, getting_poked):
		pokee = User.objects.get(id=getting_poked)
		poker = User.objects.get(id=is_poking)
		try:
			poke = Poke.objects.get(is_poking=poker,getting_poked=pokee)
			poke.single_poke_count += 1
			poke.save()
		except:
			poke = Poke.objects.create(is_poking=poker,getting_poked=pokee, single_poke_count=1)
		return pokee

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=100)
	alias = models.CharField(max_length=100)
	email = models.EmailField()
	password = models.CharField(max_length=100)
	dob = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	poke_history = models.IntegerField(default=0)
	objects = UserManager()
class Poke(models.Model):
	is_poking = models.ForeignKey(User, related_name="is_poking")
	getting_poked = models.ForeignKey(User, related_name="getting_poked")
	single_poke_count = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = PokeManager()

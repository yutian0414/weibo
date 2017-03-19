from django.db import models
from datetime import *
import hashlib
from django import forms
import time
# Create your models here.
sexset=(
		('male','male'),
		('female','female')
	)
class person(models.Model):
	"""person information which is not change very offen"""
	name=models.CharField('account name',max_length=50,unique=True)
	sex=models.CharField(max_length=10,choices=sexset)
	birth=models.DateField()
	signdate=models.DateField(auto_now_add=True)
	email=models.EmailField(null=False,unique=True)
	password=models.CharField(max_length=50)
	addressnow=models.TextField(max_length=150,default='unknown')
	localplace=models.TextField(max_length=150,default='unknown')
	motto=models.TextField(max_length=500,blank=True)
	tofind=models.BooleanField("To be find by stranges or not.",default='True')

	friend=models.ManyToManyField('self',symmetrical=False,blank=True)
	image=models.ImageField(upload_to="/media/userimage/",blank=True,null=True)
	online=models.BooleanField(default="False")


	def save(self,modify_pwd=True):
		if modify_pwd:
			md5=hashlib.md5()
			md5.update(self.password.encode('utf-8'))
			self.password=md5.hexdigest()
		else:
			pass
		super(person,self).save()

	def __str__(self):
		return self.name
	class Meat:
		db_table='person'
		permission=( )

class person_sign_up_form(forms.ModelForm):
	class Meta:
		model=person
		exclude=('signdate','friend','online')
		error_message="%(model_name)s's %(field_labels)s "



class massage(models.Model):

	fromperson=models.OneToOneField(person)
	toperson=models.CharField(max_length=50)
	textcontent=models.TextField(max_length=200,null=False,blank=False)
	filecontent=models.FileField(upload_to="./massagefile/",null=True)
	imagecontent=models.ImageField(upload_to="./massageimage/",null=True)
	createtime=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "from "+self.fromperson+" to "+self.toperson + " time "+datetime.strftime(self.createtime)




status_view_permission=(("all","all"),("friend","friend"))

class status(models.Model):

	pubtime=models.DateTimeField(auto_now_add=True)
	pubperson=models.OneToOneField(person,on_delete=models.CASCADE)
	pubtext=models.TextField(max_length=200,null=False,blank=False)
	pubimage=models.ImageField(upload_to='./pubimage/',null=True)
	viewpermission=models.CharField(max_length=5, choices=status_view_permission,default="all")

	def __str__(self):
		return "from "+self.pubperson+" time "+datetime.strftime(self.pubtime)


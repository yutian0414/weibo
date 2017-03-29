from django.db import models
from datetime import *
import hashlib
from django import forms
import time
from weibo.settings import MEDIA_ROOT
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
	image=models.ImageField(upload_to=MEDIA_ROOT+"/userimage/",blank=True,null=True)
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

	fromperson=models.ForeignKey(person,related_name='massage_from')
	toperson=models.ManyToManyField(person,related_name='massage_to')
	textcontent=models.TextField(max_length=200,null=False,blank=False)
	filecontent=models.FileField(upload_to=MEDIA_ROOT+"/massagefile/",null=True,blank=True)
	imagecontent=models.ImageField(upload_to=MEDIA_ROOT+"/massageimage/",null=True,blank=True)
	createtime=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.textcontent+self.createtime.strftime("%Y-%m-%d %H:%M:%S")




status_view_permission=(("all","all"),("friend","friend"))

class status(models.Model):

	pubtime=models.DateTimeField(auto_now_add=True)
	pubperson=models.ForeignKey(person,on_delete=models.CASCADE)
	pubtext=models.TextField(max_length=200,null=False,blank=True)
	pubimage=models.ImageField(upload_to=MEDIA_ROOT+'/pubimage/',null=True,blank=True)
	viewpermission=models.CharField(max_length=8, choices=status_view_permission,default="all")

	def __str__(self):
		return self.pubtext+self.pubtime.strftime("%Y-%m-%d %H:%M:%S")


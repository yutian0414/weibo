from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,HttpResponsePermanentRedirect
from weibo_app1.models import person,person_sign_up_form,massage,status
from datetime import datetime
from PIL import Image
import os
import time
from weibo.settings import MEDIA_ROOT
from django.views.decorators.csrf import csrf_exempt
import json
import pickle
import hashlib
from django.http import JsonResponse
from django.core.serializers import serialize
import re
# from weibo_app1.form import
# Create your views here.

def index(request):

	return render(request,'index.html')

def sign_up(request):
	if request.method=='GET':
		return render(request,'signuppage.html',{'form':person_sign_up_form})
	if request.method=="POST":
		form=person_sign_up_form(request.POST)
		print(form)
		print(request.POST.get('birth'))
		print(form.is_valid())
		if form.is_valid():
			sign_up_data=form.save(commit=False)
			sign_up_data.signdate=datetime.now()
			sign_up_data.online=True
			sign_up_data.image=imagesave(request)
			sign_up_data.save()
			md5=hashlib.md5()
			print(sign_up_data.image)
			return HttpResponseRedirect('/home/')
		else:

			return render(request,'signuppage.html',{'form':form})

def home(request,*args):
	print(args)
	user=person.objects.get(name=args[0])
	if args[1]==user.password:
		print(user,type(user),user.image,type(user.image))
		request.session['username']=args[0]
		status_of_friends=[]
		status_ordered=status.objects.order_by("pubtime")
		for statu in status_ordered:
			if statu.pubperson in user.friend.all():
				status_of_friends.append(statu)
		print("statu:",statu)
		chart_with=[]
		chart_massage=[]
		massages_ordered=massage.objects.order_by('createtime')
		templist=[]

		for masg in massages_ordered:
			if masg.toperson==user:
				l=[]
				for i in masg.fromperson.all():
					l.append(i.name)
				if l not in templist:
					chart_with.append(masg.fromperson.all())
					templist.append(l)
				chart_massage.append(masg_dict)
			elif masg.fromperson==user:
				l=[]
				for i in masg.toperson.all():
					l.append(i.name)
				if l not in templist:
					chart_with.append(masg.toperson.all())
					templist.append(l)
				chart_massage.append(masg)

		chart_with=set(chart_with)
		return render(request,'home.html',{'user':user,"status":status_of_friends,"chart_with":chart_with,"chart_massage":chart_massage,"chart_friend_name":templist})
	else:
		return HttpResponseRedirect('/sign_in/')




@csrf_exempt
def sign_in(request):

	if request.is_ajax():
		if request.method=="POST":
			username=request.POST["name"]
			userpassword=request.POST["password"]
			print(username,userpassword)
			try:
				user=person.objects.get(name=username)
			except:
				user=None
			if user:
				md5=hashlib.md5()
				md5.update(userpassword.encode("utf-8"))
				userpassword=md5.hexdigest()
				print(user)
				print(user.password==userpassword,user.password,userpassword)
				if user.password==userpassword:
					print(user,type(user))
					#user.friend.all()
					userinfo={"username":user.name,"password":user.password}
					return JsonResponse(userinfo)
				else:
					return JsonResponse({"password":"False"})
			else:
				return JsonResponse({"username":"False"})



def imagesave(request):
	print(request)
	imagedata=request.FILES.get('image')
	name=request.POST.get('name')
	print(imagedata)
	try:
		im=Image.open(imagedata)
	except AttributeError:
		print("imagedata is None")
		return ''
	imagepath=os.path.abspath(MEDIA_ROOT+r"/userimage/")
	imagename=name+str(time.strftime("%Y-%m-%d",time.localtime()))+'.PNG'
	im.save('%s/%s' %(imagepath,imagename),'PNG')
	print(imagepath+imagename)
	return r"/userimage/"+r"/"+imagename

@csrf_exempt
def chart_with_rescently(request):
	if request.is_ajax():
 		if request.method=="POST":
 			username=request.POST["username"]
 			print(username+"11111111111111111")
 			user=person.objects.get(name=username)
 			fromperson=list(massage.objects.filter(fromperson=user))
 			toperson=list(massage.objects.filter(toperson=user))
 			print(fromperson,toperson)
 			chart_with=[]
 			for per_to in fromperson:
 				chart_with.append(per_to.toperson)
 			for per_from in toperson:
 				chart_with.append(per_from)
 			chart_with=json.dumps(list(set(chart_with)))
 			print(chart_with)
 			return JsonResponse({"friend_list":chart_with})

def logout(request):
	try:
		del request.session["username"]
	except KeyError:
		pass
	return HttpResponse("You're logged out")

@csrf_exempt
def getcharthistory(request):
	if request.is_ajax():
		if request.method=="POST":
			username=request.POST["username"]
			friendname_list=re.split(r'\s\|\s',request.POST["friend_list"])
			friend_list=[]
			print(friendname_list)
			username=person.objects.get(name=username)
			for j in friendname_list:
				friend_list.append(person.objects.get(name=j))
			query1=massage.objects.filter(fromperson__exact=username)
			query2=massage.objects.filter(toperson__exact=username)
			for i in friendname_list:
				query1=query1.filter(toperson__exact=i)
				query2=query2.filter(toperson__exact=i)

			masg=query1 | query2
			print("masg::",masg)
			masg=masg.distinct()
			masg=masg.order_by('createtime')
			masg_dic_temp=massage_to_dic(masg)
			print(masg_dic_temp)
			masg_dic={}
			for item,val in masg_dic_temp.items():
				if val["fromperson"]==username.name:
					if len(val["toperson"])!=len(friend_list):
						pass
					else:
						masg_dic[item]=val
				elif username.name in val['toperson']:
					if len(val['toperson'])!=len(friend_list):
						pass
					else:
						masg_dic[item]=val
				else:
					raise ValueError("ERROR")

			response=JsonResponse(masg_dic,safe=False)
			response['Access-Control-Allow-Origin']='*'
			return response

@csrf_exempt
def sendmassage(request):
	if request.is_ajax():
		if request.method=="POST":
			username=request.POST['username']
			topersonname=request.POST['sendto']
			textcontent=request.POST['text']
			fromperson=person.objects.get(name=username)
			toperson=[]
			for pe in re.split(r"\s\|\s",topersonname):
				print(pe,len(pe),type(pe))
				try:
					toperson.append(person.objects.get(name=pe))
				except:
					toperson=[]
					break
			if textcontent!='' and toperson:
				massage_get=massage()
				massage_get.fromperson=fromperson
				createtime=datetime.now()
				print(toperson)

				massage_get.textcontent=textcontent
				massage_get.createtime=createtime
				massage_get.save()
				for e in toperson:
					massage_get.toperson.add(e)
				massage_get.save()
				return JsonResponse({'sended':"Sended",'textcontent':textcontent,'createtime':createtime})
			else:
				masg=massage.objects.filter(toperson=username)
				masg_dic=massage_to_dic(masg)
				response=JsonResponse(masg_dic,safe=False)
				response['Access-Control-Allow-Origin']='*'

				return response

def massage_to_dic(masg):
	masg_dic={}
	temp={}
	j=0
	for i in masg:

		print(i)
		name=[]
		temp={}
		print(i.toperson.all())
		for em in i.toperson.all():
			name.append(em.name)
		temp["toperson"]=name
		temp['fromperson']=str(i.fromperson_id)
		temp['createtime']=str(i.createtime)
		temp['textcontent']=i.textcontent
		temp['filecontent']=str(i.filecontent)
		temp['imagecontent']=str(i.imagecontent)

		masg_dic[str(j)]=temp
		j=j+1
	print(masg_dic)
	return masg_dic
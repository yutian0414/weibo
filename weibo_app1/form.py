from django import forms

class person_sign_up_form(forms.Form):
	name=forms.CharField(max_length=50,required=True,error_messages={'value':'error'})
	sexset=(("male","male"),("female","female"))
	sex=forms.CharField(widget=forms.widgets.Select(choices=sexset,attrs={'class':'form-control'}),error_messages={'value':'error'})
	birth=forms.DateField(error_messages={'value':'error'})

	email=forms.EmailField(required=True,error_messages={'value':'error'})
	password=forms.CharField(max_length=50,required=True,error_messages={'value':'error'})
	addressnow=forms.CharField(max_length=150,error_messages={'value':'error'})
	localplace=forms.CharField(max_length=150,error_messages={'value':'error'})
	motto=forms.CharField(max_length=500,error_messages={'value':'error'})
	tofind=forms.BooleanField("To be find by stranges or not.",error_messages={'value':'error'})


	image=forms.ImageField(error_messages={'value':'error'})

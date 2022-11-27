from django import forms
from django.forms import ModelForm, widgets
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from SingventoryApp.models import SVUser, Equipment, Borrow, Category
from django import forms
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only string')

class SVUserForm(ModelForm):

    name = forms.CharField(max_length=20,validators=[alphanumeric],widget=forms.TextInput(
        attrs={
        'class': "form-control", 'title':'Name should contain only string.','pattern':'[A-Za-z]+',
        
    }))

   
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': "form-control", 'required':'', 'type':'email', 'name':'email'

    }))

 
    password1 = forms.CharField(min_length=6,widget=forms.PasswordInput(attrs={
        'class': "form-control", 'id':'pwd','required':'','type':'password', 'name':'password'

    }))

    password2 = forms.CharField(min_length=6,widget=forms.PasswordInput(attrs={
        'class': "form-control", 'id':'pwd', 'required':'', 'type':'password',

    }))


    class Meta:
        
        model = SVUser
        fields = ['name','email','password1','password2']

        
class SVUserFormAdmin(ModelForm):

    name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': "form-control", 'required':'','type':'text',
        
    }))

   
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': "form-control", 'required':'', 'type':'email',

    }))

 
    password1 = forms.CharField(min_length=6,widget=forms.PasswordInput(attrs={
        'class': "form-control", 'id':'pwd','required':'','type':'password',

    }))

    password2 = forms.CharField(min_length=6,widget=forms.PasswordInput(attrs={
        'class': "form-control", 'id':'pwd', 'required':'', 'type':'password',

    }))

    category = forms.Select(attrs={
        'class': "form-select",'required':'', 'type':'select',

    })

    class Meta:
        
        model = SVUser
        fields = ['name','email','password1','password2','category']
        widgets = {
            'category':forms.Select(attrs={'class':'form-select'})
        }
    
class BorrowForm(ModelForm):

    class Meta:
        model = Borrow
        fields = ['user','equipment','quantity']
        widgets = {
            'quantity':forms.NumberInput(attrs={'class':'form-control','placeholder':'Quantity'})
        }

class UserUpdateForm(ModelForm):
    name = forms.CharField(max_length=32, widget=forms.TextInput(attrs={
        'class': "form-control", 'required':'','type':'text',
        
    }))

   
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': "form-control", 'required':'', 'type':'email',

    }))


    class Meta:
        
        model = SVUser
        fields = ['name','email','image']
        widgets ={
            'name':forms.TextInput(attrs={'class':'form-control','required':''}),
            'description':forms.EmailInput(attrs={'class':'form-control','required':''}),
            'image':forms.FileInput(attrs={'class':'form-control','accept':'image/*'})
        }

class CategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'quantity':forms.TextInput(attrs={'class':'form-control', 'required':'',})
        }

class EquipmentForm(ModelForm):

    class Meta:
        model= Equipment
        fields = ['name', 'description', 'quantity','image', 'category']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Item Name'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Description','rows':'3'}),
            'image':forms.FileInput(attrs={'class':'form-control','accept':'image/*'}),
            'quantity':forms.NumberInput(attrs={'class':'form-control','placeholder':'Price'}),
            'category':forms.Select(attrs={'class':'form-select','placeholder':'Category'}),

        }
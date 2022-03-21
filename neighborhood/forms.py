from  django import  forms
from .models import *

class  Neighbohoodform(forms.ModelForm):
    models=Neighborhood
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['username','joined']
        

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        exclude=['username','profile_image', 'publishedAt']
    
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        exclude=['username','post']
    
class ShopForm(forms.ModelForm):
    class Meta:
        model=Shop
        exclude=['owner','neighborhood']
    
class AlertsForm(forms.ModelForm):
    class Meta:
        model=Alerts
        exclude=['author','neighbourhood','post_date']
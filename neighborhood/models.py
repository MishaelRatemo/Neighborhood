from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import  User
from cloudinary.models import CloudinaryField


alert_prio=(
            ('High','High Priority'),
            ('Medium','Medium Priority'),
            ('Low','Low Priority'),           
                
            )
class Neighborhood(models.Model):
    neighborhood = models.CharField(max_length=60)
    
    def __str__(self):
        return  self.neighborhood
    
    def create_neighborhood(self):
        self.save()
    @classmethod
    def update_neighborhood(cls,neighborhood):
        cls.objects.filter(neighborhood=neighborhood).update()
        
    @classmethod
    def delete_neighbourhood(cls,neighbourhood):
        cls.objects.filter(neighbourhood=neighbourhood).delete()
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = CloudinaryField('image')    
    bio = models.TextField(max_length=500, default="My Bio", blank=True)
    full_name =models.CharField(max_length=50)
    location = models.CharField(max_length=60, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    phone = models.CharField(max_length=16,blank=True)
    neighborhood = models.ForeignKey(Neighborhood,on_delete=models.CASCADE)
    joined =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save_profile(self):
        super().save()
        
    @classmethod
    def get_profile_by_id(cls,id):
        profile = Profile.objects.get(user = id)
        return profile
    
    @classmethod
    def filter_profile_by_id(cls,id): 
        profile = Profile.objects.filter(user = id).first()
        return profile
    
class Post(models.Model):
    title = models.CharField(max_length=80)
    image = CloudinaryField('image')
    post = HTMLField()
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    neighborhood= models.ForeignKey(Neighborhood,on_delete=models.CASCADE)
    publishedAt = models.DateTimeField(auto_now_add=True)
    profile_image = models.ForeignKey(Profile,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def save_post(self):
        self.save()
        
class Comment(models.Model):
    comment = models.CharField(max_length=255)
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    
    def save_comment(self):
        self.save()
    
    @classmethod
    def delete_comment(cls,comment):
        cls.objects.filter(comment=comment).delete()
        
class Healthservice(models.Model):
    healthservices = models.CharField(max_length=100)

    def __str__(self):
        return self.healthservices

    def save_healthservices(self):
        self.save()

    @classmethod
    def delete_healthservices(cls,healthservices):
        cls.objects.filter(healthservices=healthservices).delete()
        
class Health(models.Model):
    logo = CloudinaryField('image')
    neighborhood = models.ForeignKey(Neighborhood,on_delete=models.CASCADE)
    name =models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.IntegerField()
    address =models.CharField(max_length=100)
    healthservices = models.ManyToManyField(Healthservice)

    def __str__(self):
        return self.name
    
    def save_health(self):
        self.save()
        
class Shop(models.Model):
    logo = CloudinaryField('image')
    shop_name =models.CharField(max_length=100)
    description = HTMLField()
    neighborhood = models.ForeignKey(Neighborhood,on_delete=models.CASCADE)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    email = models.EmailField()
    address =models.CharField(max_length=100)
    contact = models.IntegerField()

    def __str__(self):
        return self.name
    
    @classmethod
    def search_business(cls,search_term):
        business = cls.objects.filter(shop_name__icontains=search_term)
        return business
class Administration(models.Model):
    neighborhood = models.ForeignKey(Neighborhood,on_delete=models.CASCADE)
    name =models.CharField(max_length=50)
    email = models.EmailField()
    contact = models.IntegerField()
    address =models.CharField(max_length=60)

    def __str__(self):
        return self.name
    
    def save_administration(self):
        self.save()
        
    @classmethod
    def delete_administration(cls,administration):
        cls.objects.filter(name=administration).delete()
        
class Alerts(models.Model):
    alert_title = models.CharField(max_length=100)
    notification = HTMLField()
    priority = models.CharField(max_length=15,choices=alert_prio,default="---Select---")
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    neighbourhood = models.ForeignKey(Neighborhood,on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.alert_title

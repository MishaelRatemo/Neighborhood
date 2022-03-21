from django.contrib import admin
from .models import Post, Profile, Alerts, Shop, Administration, Comment,Neighborhood,Health,Healthservice
# Register your models here.
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Alerts)
admin.site.register(Shop)
admin.site.register(Administration)
admin.site.register(Comment)
admin.site.register(Neighborhood)
admin.site.register(Health)
admin.site.register(Healthservice)
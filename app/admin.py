from django.contrib import admin
from .models import Category,Destination,Destination_detail,BookNow
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name']
    
@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display=['id','title','popular']
    
    
@admin.register(Destination_detail)
class Destination_detailAdmin(admin.ModelAdmin):
    list_display=['id','destinationid','discription']

@admin.register(BookNow)
class BookNowAdmin(admin.ModelAdmin):
    list_display=["id",'user','destination','child','adults','kids','start_date','end_date']

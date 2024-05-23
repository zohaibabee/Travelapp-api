from django.db import models
from accounts.models import User
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.name



    
class Destination(models.Model):
    title=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    price_per_person= models.IntegerField()
    popular=models.BooleanField(default=False)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)
    
class Destination_detail(models.Model):
    destinationid=models.OneToOneField(Destination,on_delete=models.CASCADE)
    discription=models.TextField()
    main_image=models.ImageField(upload_to='mymedia')
    image2=models.ImageField(upload_to='mymedia',blank=True)
    image3=models.ImageField(upload_to='mymedia',blank=True)
    image4=models.ImageField(upload_to='mymedia',blank=True)
    has_wifi=models.BooleanField(default=True)
    has_dinner=models.BooleanField(default=True)
    has_tub=models.BooleanField(default=True)
    has_pool=models.BooleanField(default=True)
    def __str__(self):
        return str(self.id)
    
    

    

class BookNow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    child = models.PositiveIntegerField(default=0)
    adults = models.PositiveIntegerField(default=1)
    kids = models.PositiveIntegerField(default=0)
    start_date=models.DateField()
    end_date=models.DateField()
    
    def __str__(self):
        return f'{self.user.email}'
    
    
        
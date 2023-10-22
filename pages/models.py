from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
class RecordTransaction(models.Model):
    transaction_id = models.IntegerField()
    customer_name = models.CharField(max_length=20)
    contact_number = models.IntegerField()
    transaction_amount = models.FloatField()
    transaction_date = models.DateField()
    payment_method = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    actions = models.CharField(max_length=100)
    
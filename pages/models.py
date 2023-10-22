from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

class PaymentMethod(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name

class RecordTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=20, unique=True)
    transaction_amount = models.FloatField()
    transaction_date = models.DateField()
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    actions = models.TextField()
    
from django.contrib import admin
from .models import Profile, PaymentMethod, Category, RecordTransaction, Goal # Import your model classes here

# Create a list of model classes you want to register
models_to_register = [Profile, PaymentMethod, Category, RecordTransaction, Goal]  # Add your models to this list

# Register all the models in the list
for model in models_to_register:
    admin.site.register(model)


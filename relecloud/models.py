from django.db import models
from django.core.exceptions import ValidationError
from django import forms
from storages.backends.azure_storage import AzureStorage
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.db.models import Avg  # For calculating average ratings


# Azure Storage Configuration
class AzureMediaStorage(AzureStorage):
    account_name = "mediarelecloud"  
    account_key = "+gTybudYJWptj2autzr7b4Z6UFfXHE0rkAxf/ta2aMIrH34u1IVhkdO7QkDLOCwkLwr5D8xLEA5h+AStQk4GIg=="
    azure_container = "media"
    expiration_secs = None  
    token_sas = "sp=racwdli&st=2024-12-20T19:02:09Z&se=2026-07-01T02:02:09Z&sv=2022-11-02&sr=c&sig=egpPARZwfYT%2F1jHBeTqQEW0PrgFXVkaXXJvsYG7Yi8g%3D"

    def url(self, name):
        base_url = super().url(name)
        return f"{base_url}?{self.token_sas}"  


# Trip Model (Assumed)
class Trip(models.Model):
    destination = models.ForeignKey('Destination', related_name='trips', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def _str_(self):
        return self.name


# Destination Model
class Destination(models.Model):
    name = models.CharField(unique=True, null=False, blank=False, max_length=50)
    description = models.TextField(max_length=2000, null=False, blank=False)
    slug = models.SlugField()
    image = models.ImageField(storage=AzureMediaStorage(), upload_to='destinations/', null=True, blank=True)

    # Method to calculate the average rating
    def average_rating(self):
        reviews = self.reviews.all()  # Reverse relation from the Review model
        return reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    # Validate if a destination can have reviews (must have at least one trip)
    def can_have_reviews(self):
        if not self.trips.exists():
            raise ValidationError("Destinations without trips cannot have reviews.")

    def save(self, *args, **kwargs):
        self.can_have_reviews()  # Ensure the destination can have reviews before saving
        super().save(*args, **kwargs)

    def _str_(self):
        return self.name
        

# Cruise Model
class Cruise(models.Model):  
    name = models.CharField(unique=True, null=False, blank=False, max_length=50)
    description = models.TextField(max_length=2000, null=False, blank=False)
    destinations = models.ManyToManyField(Destination, related_name='cruises')
    image = models.ImageField(storage=AzureMediaStorage(), upload_to='cruises/', null=True, blank=True)

    def average_rating(self):
        reviews = self.reviews.all()
        return reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    def _str_(self):
        return self.name


# Review Model
class Review(models.Model):
    destination = models.ForeignKey(Destination, related_name="reviews", on_delete=models.CASCADE, null=True, blank=True)
    cruise = models.ForeignKey(Cruise, related_name="reviews", on_delete=models.CASCADE, null=True, blank=True)
    user_name = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.IntegerField()

    def _str_(self):
        return f"{self.user_name} - {self.rating}"


# InfoRequest Model
class InfoRequest(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField()
    notes = models.TextField(max_length=2000, null=False, blank=False)
    cruise = models.ForeignKey(Cruise, on_delete=models.PROTECT)
    

# FORMS

# InfoRequest Form
class InfoRequestForm(forms.ModelForm):
    class Meta:
        model = InfoRequest
        fields = ['name', 'email', 'cruise', 'notes']

    def _init_(self, *args, **kwargs):
        super(InfoRequestForm, self)._init_(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))


# Destination Form
class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'description', 'slug', 'image']

    def _init_(self, *args, **kwargs):
        super(DestinationForm, self)._init_(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Destination'))


# Cruise Form
class CruiseForm(forms.ModelForm):
    class Meta:
        model = Cruise
        fields = ['name', 'description', 'destinations', 'image']

    def _init_(self, *args, **kwargs):
        super(CruiseForm, self)._init_(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Cruise'))


# Review Form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user_name', 'comment', 'rating']

    def _init_(self, *args, **kwargs):
        super(ReviewForm, self)._init_(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Review'))
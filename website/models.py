from django.db import models

# Create your models here.


class BlogPost(models.Model):
    id = models.AutoField(primary_key=True)
    public = models.BooleanField(default=False)
    title = models.TextField(blank=False)
    content = models.TextField(blank=False)
    img = models.TextField(default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDfEj8ozDOs68NfqOABBKIOZSXTrYvjClYxeESyd09NE5DRAmcIYoZTJeRhBU&s")
    date = models.DateField(auto_now_add=True)

class GroceryItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

class FunThing(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

class Chore(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

class ThingToBuy(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
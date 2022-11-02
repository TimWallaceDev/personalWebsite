from django.db import models

# Create your models here.

class Blacklist(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=25)

class Whitelist(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=25)


class TopWords(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=25)
    date = models.DateField(auto_now_add=True)

class TopWordsByOrg(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=25)
    org = models.CharField(max_length=25)
    date = models.DateField(auto_now_add=True)

class DeepArchive(models.Model):
    id = models.AutoField(primary_key=True)
    org = models.CharField(max_length=25)
    word = models.CharField(max_length=25)
    count = models.IntegerField()
    date = models.IntegerField()

class BoneBrothArchive(models.Model):
    id = models.AutoField(primary_key=True)
    org = models.CharField(max_length=25)
    word = models.CharField(max_length=25)
    count = models.IntegerField()
    date = models.IntegerField()

class Millions(models.Model):
    id = models.AutoField(primary_key=True)
    headline = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    
class ThirtyThrees(models.Model):
    id = models.AutoField(primary_key=True)
    headline = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
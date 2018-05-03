from __future__ import unicode_literals
from django.db import models
# Create your models here.

class Articles(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField(max_length = 255)
    source = models.CharField(max_length=255)
    post_date = models.DateTimeField()
    found_date = models.DateTimeField()
    title = models.CharField(max_length=255)
    author = models.TextField()
    keywords = models.CharField(max_length=255, blank=True)
    summary = models.TextField(null=True)
    text = models.TextField()
    top_image = models.URLField(null=True, max_length = 500)
    video = models.URLField(null=True)


class People(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=45)
    first_name = models.CharField(max_length=45)
    person_id = models.CharField(max_length=45, null=True)
    party = models.CharField(max_length=45)
    role = models.CharField(max_length=45)
    legislative_since = models.CharField(max_length=255, null=True)
    image = models.URLField(null=True)
    biography = models.CharField(max_length=45, null=True)
    district = models.CharField(max_length=45, null=True)
    counties = models.CharField(max_length=255, null=True)
    profession = models.CharField(max_length=255, null=True)
    profession_affiliations = models.TextField(null=True)
    education = models.CharField(max_length=255, null=True)
    recognitions_and_honors = models.TextField(null=True)
    home_phone = models.CharField(max_length=45, null=True)
    work_phone = models.CharField(max_length=45, null=True)
    cell = models.CharField(max_length=45, null=True)
    email = models.EmailField(null=True)
    social_media = models.CharField(max_length=45,null=True)
    legislation_link = models.URLField(null=True)
    mailing_address = models.CharField(max_length=255)
    committies = models.CharField(max_length=45, null=True)
    social_media = models.CharField(max_length=45, null=True)

class Article_Person(models.Model):
    articles_id = models.ForeignKey('Articles', on_delete=models.CASCADE)
    people_id = models.ForeignKey('People', on_delete=models.CASCADE)
    weight = models.DecimalField(null=True, max_digits=19, decimal_places=4)
    name_mentions = models.IntegerField(default=0, null=True)
    mention_percentage = models.IntegerField(default=0, null=True)
    article_total_count_mentions = models.IntegerField(default=0, null=True)

class Bills(models.Model):
    bill_name_id = models.IntegerField(primary_key=True)
    bill_type_choices = (
        ('HB','House Bill'),
        ('nHCR','House Concurrect Resolutions'),
        ('nHJR','House Joint Resolutions'),
        ('nHR','House Resolutions'),
        ('nSB','Senate Bills'),
        ('nSCR','Senate Concurrent'),
        ('nSJR','Senate Joint Resolutions'),
        ('nSR','Senate Resolutions')
        )
    bill_type = models.CharField(max_length=100, choices=bill_type_choices)
    sponser = models.CharField(max_length=45, blank=True)
    floor_sponser = models.CharField(max_length=45, blank=True)
    substitute_sponser = models.CharField(max_length=45, null=True)
    last_action = models.CharField(max_length=45, null=True)
    last_location = models.CharField(max_length=45, null=True)
    text = models.CharField(max_length=45, null=True)

class Bill_Status(models.Model):
    bill_name_id = models.ForeignKey('Bills')
    date = models.DateTimeField()
    action = models.CharField(max_length=45)
    location = models.CharField(max_length=45)
    vote = models.CharField(max_length=45,blank=True)
    who_acted_choices = (
        ('SA', 'Senate Actions'),
        ('HA', 'House Actions'),
        ('FA', 'Fiscal Actions'),
        ('OA', 'Other Actions')
        )
    who_acted = models.CharField(max_length=45, choices=who_acted_choices)

class Article_Bill(models.Model):
    articles_id = models.ForeignKey('Articles')
    bill_name_id = models.ForeignKey('Bills')
    weight = models.IntegerField(null=True)

class Person_Bill(models.Model):
    people_id = models.ForeignKey('People')
    bill_name_id = models.ForeignKey('Bills')

class Location(models.Model):
    idlocations = models.IntegerField(primary_key=True)
    location = models.CharField(max_length= 45, blank=True)

class Article_Location(models.Model):
    articles_id = models.ForeignKey('Articles')
    idlocaiton = models.ForeignKey('Location')
    weight = models.IntegerField(null=True)
    location_mentions = models.IntegerField(default=0, null=True)
    mention_percentage = models.IntegerField(default=0, null=True)
    place_mention_total = models.IntegerField(default=0, null=True)

class Article_Based_Weights(models.Model):
    articles_id = models.ForeignKey('Articles')
    length = models.IntegerField(null=True)
    source_size_ration = models.IntegerField(null=True)
    is_local = models.CharField(max_length=45, null=True)

class Committies(models.Model):
    idcommitties = models.AutoField(primary_key=True)
    committie = models.CharField(max_length=255)
    overview = models.TextField(null=True)

class Person_Committies(models.Model):
    people_id = models.ForeignKey('People')
    idcommitties = models.ForeignKey('Committies')
    position = models.CharField(max_length= 45, null=True)

class Bill_Weight(models.Model):
    articles_id = models.ForeignKey('Articles')
    bill_name_id = models.ForeignKey('Bills')
    location_mentions = models.IntegerField(null=True)
    mention_percentage = models.IntegerField(null=True)

class Social_Media(models.Model):
    articles_id = models.ForeignKey('Articles')
    facebook_shares = models.IntegerField(default=0, null=True)
    facebook_comments = models.IntegerField(default=0, null=True)
    reddit_shares = models.IntegerField(default=0, null=True)
    reddit_upvotes = models.IntegerField(default=0, null=True)
    pinterest_pins = models.IntegerField(default=0, null=True)
    linkedin_shares = models.IntegerField(default=0, null=True)
    total_count = models.IntegerField(default=0, null=True)

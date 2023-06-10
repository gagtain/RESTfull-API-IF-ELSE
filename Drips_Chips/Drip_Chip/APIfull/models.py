from django.db import models
from .custom_valid import No_equal_to, locations_validate


class MyUser(models.Model):
    firstName = models.CharField('firstName', max_length=140)
    lastName = models.CharField('lastName', max_length=140)
    email = models.EmailField('email', unique=True)
    password = models.CharField('пароль', max_length=140)

    def __str__(self):
        return self.email

class AnimalsType(models.Model):
    type = models.CharField('type', max_length=140)

class locations(models.Model):
    latitude = models.FloatField(validators=[locations_validate(90)])
    longitude = models.FloatField(validators=[locations_validate(180)])

class AnimalsLocationVisit(models.Model):
    locationPointId = models.ForeignKey(locations, on_delete=models.CASCADE)
    dateTimeOfVisitLocationPoint = models.DateTimeField(auto_now_add=True)



class visitedLocationsM2M(models.Model):
    AnimalsLocationVisit = models.ForeignKey(AnimalsLocationVisit, on_delete=models.CASCADE)
    Animals = models.ForeignKey('Animals', on_delete=models.CASCADE)




class Animals(models.Model):

    class LIVE_CHOICES(models.TextChoices):
        ALIVE = "ALIVE", "ALIVE"
        DEAD = "DEAD", "DEAD"


    class GENDERS_CHOICES(models.TextChoices):
        MALE = "MALE", "MALE"
        FEMALE = "FEMALE", "FEMALE"
        OTHER = "OTHER", "OTHER"

    animalTypes = models.ManyToManyField(AnimalsType, related_name='animalTypes_list')
    weight = models.FloatField(validators=[No_equal_to(0)])
    length = models.FloatField(validators=[No_equal_to(0)])
    height = models.FloatField(validators=[No_equal_to(0)])
    gender = models.CharField(max_length=21, choices=GENDERS_CHOICES.choices)
    lifeStatus = models.CharField(max_length=21, choices=LIVE_CHOICES.choices, blank=True, default='ALIVE')
    chippingDateTime = models.DateTimeField(auto_now_add=True)
    chipperId = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='chipperID')
    chippingLocationId = models.ForeignKey(locations, on_delete=models.CASCADE, related_name='chippingLocationId_list')
    visitedLocations = models.ManyToManyField(AnimalsLocationVisit, related_name='visitedLocations', blank=True, through='visitedLocationsM2M')
    deathDateTime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.lifeStatus



from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="person")

    name = models.TextField()
    depressions = models.IntegerField()

    friends: models.ManyToManyField = models.ManyToManyField('self', blank=True)
    friends_requests: models.ManyToManyField = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return str(self.name)


@receiver(post_save, sender=User)
def create_profile(sender, instance: User, created, **kwargs):
    if created:
        pers = Person.objects.create(user=instance, depressions=0)
        pers.name = instance.get_username()
        pers.depressions = 0
        pers.save()
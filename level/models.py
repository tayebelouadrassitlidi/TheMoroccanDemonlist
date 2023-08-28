from django.db import models
import math
from django.contrib import admin
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Level(models.Model):

    DIFFICULTIES = [
        ('Hard Demon', 'Hard Demon'),
        ('Insane Demon', 'Insane Demon'),
        ('Extreme Demon', 'Extreme Demon'),
    ]

    DURATIONS = [
        ('Tiny', 'Tiny'),
        ('Short', 'Short'),
        ('Medium', 'Medium'),
        ('Long', 'Long'),
        ('XL', 'XL'),
    ]

    levelid = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    ranking = models.PositiveIntegerField(default=0, db_index=True)
    difficulty = models.CharField(max_length=255, choices=DIFFICULTIES,)
    duration = models.CharField(max_length=255, choices=DURATIONS,)
    youtube_link = models.URLField(blank=True)
    youtube_thumbnail = models.URLField(blank=True)
    points = models.FloatField(default=0)
    min_points = models.FloatField(default=0)
    min_completion = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    first_victor = models.ForeignKey('player.Player', on_delete=models.PROTECT, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.ranking is not None:
            self.points = round(500 * (1 - math.log(self.ranking, 151)), 2)
            self.min_points = round((500 * (1 - math.log(self.ranking, 151))) * 1/3, 2)
        else:
            self.points = None
            self.min_points = None

        super(Level, self).save(*args, **kwargs)

    def __str__(self):
        return f"#{self.ranking} - {self.name}"

@receiver(post_save, sender='player.Player')
@receiver(post_save, sender='levelrecord.LevelRecord')
def update_region_points(sender, instance, **kwargs):
    from player.models import Player
    from levelrecord.models import LevelRecord
    
    if isinstance(instance, Player):
        region = instance.region
    elif isinstance(instance, LevelRecord):
        region = instance.player.region
    
    region.points = region.calculate_points()
    region.save()

@receiver(post_save, sender=Level)
def create_level_record(sender, instance, created, **kwargs):
    from levelrecord.models import LevelRecord
    if created and instance.first_victor:
        player = instance.first_victor
        level_record = LevelRecord.objects.create(player=player, level=instance, record_percentage=100)

@receiver(post_save, sender=Level)
def update_min_completion(sender, instance, **kwargs):
    if instance.ranking > 75 and instance.min_completion != 100:
        instance.min_completion = 100
        instance.save(update_fields=['min_completion'])
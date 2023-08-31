from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from level.models import Level

# Create your models here.

class ListChange(models.Model):

    place = 'Place'
    #move = 'Move'
    raise_ = 'Raise'
    lower = 'Lower'
    swap = 'Swap'
    remove = 'Remove'
    list_requirement = 'List requirement'

    CHANGE_TYPE = [
        ('Place', 'Place'),
        #('Move', 'Move'),
        ('Raise', 'Raise'),
        ('Lower', 'Lower'),
        ('Swap', 'Swap'),
        ('Remove', 'Remove'),
        ('List requirement', 'List requirement'),
    ]

    level = models.ForeignKey(Level, on_delete=models.PROTECT)
    #swap_with = models.ForeignKey(Level, related_name='swap_with', on_delete=models.CASCADE, blank=True)
    date = models.DateField()
    change_type = models.CharField(max_length=255, choices=CHANGE_TYPE, default=None)
    placement = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=255, blank=True)
    above_level = models.ForeignKey(Level, related_name='above_level', on_delete=models.PROTECT, blank=True, null=True)
    below_level = models.ForeignKey(Level, related_name='below_level', on_delete=models.PROTECT, blank=True, null=True)
    effect = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Change for Level {self.level.name} on {self.date}"
    
@receiver(pre_save, sender=ListChange)
def populate_description(sender, instance, **kwargs):
    if instance.change_type == ListChange.place:
        instance.description = f"{instance.level.name} has been placed at #{instance.placement}"
    #elif instance.change_type == ListChange.move:
        #instance.description = f"{instance.level.name} has been moved to #{instance.placement}"
    elif instance.change_type == ListChange.swap:
        instance.description = f"{instance.level.name} has been swapped with #{instance.swap_with.name} at #{instance.placement}"
    elif instance.change_type == ListChange.raise_:
        instance.description = f"{instance.level.name} has been raised to #{instance.placement}"
    elif instance.change_type == ListChange.lower:
        instance.description = f"{instance.level.name} has been lowered to #{instance.placement}"
    elif instance.change_type == ListChange.remove:
        instance.description = f"{instance.level.name} has been removed"
    elif instance.change_type == ListChange.list_requirement:
        instance.description = f"{instance.level.name}'s list requirement has been changed to #{instance.level.min_completion}"

    if instance.above_level is not None:
        instance.description += f", above {instance.above_level.name}"
    if instance.below_level is not None and instance.above_level is not None:
        instance.description += f" and below {instance.below_level.name}"
    if instance.below_level is not None and instance.above_level is None:
        instance.description += f", below {instance.below_level.name}"

    instance.description += "."
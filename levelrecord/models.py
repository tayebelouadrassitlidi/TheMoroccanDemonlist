from django.db import models
from player.models import Player
from level.models import Level
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class LevelRecord(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    record_percentage = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    record_video_link = models.URLField(blank=True)
    
    class Meta:
        unique_together = ['level', 'player']

    def update_player_points(self):
        level = self.level
        player = self.player
        record_percentage = self.record_percentage

        if record_percentage == 100:
            points = level.points
        elif level.min_completion < record_percentage < 100:
            points = level.min_points

        if player.points != points:
            player.points = points
            player.save(update_fields=['points'])

    def save(self, *args, **kwargs):
        if self.pk is None:
            if not self.level.first_victor or self.record_percentage == 100:
                self.level.first_victor = self.player
                self.level.save()

        super(LevelRecord, self).save(*args, **kwargs)
        self.update_player_points()

    def __str__(self):
        return f"{self.player.name} - {self.level.name} ({self.record_percentage}%)"

@receiver(post_save, sender=LevelRecord)
def update_player_points_signal(sender, instance, **kwargs):
    instance.update_player_points()
from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100)
    points = models.FloatField(default=0)

    def calculate_points(self):
        total_points = 0

        for player in self.player_set.all():
            total_points += player.points

        return total_points

    def __str__(self):
        return f"{self.name} - {round(self.points, 2)} points"
# Generated by Django 4.2.4 on 2023-08-25 11:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('levelid', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('creator', models.CharField(max_length=255)),
                ('difficulty', models.CharField(choices=[('Hard Demon', 'Hard Demon'), ('Insane Demon', 'Insane Demon'), ('Extreme Demon', 'Extreme Demon')], max_length=255)),
                ('ranking', models.IntegerField(blank=True)),
                ('duration', models.CharField(choices=[('Tiny', 'Tiny'), ('Short', 'Short'), ('Medium', 'Medium'), ('Long', 'Long'), ('XL', 'XL')], max_length=255)),
                ('objectcount', models.CharField(blank=True, max_length=255)),
                ('youtube_link', models.URLField(blank=True)),
                ('youtube_thumbnail', models.URLField(blank=True)),
                ('points', models.FloatField(default=0)),
                ('min_points', models.FloatField(default=0)),
                ('min_completion', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)])),
                ('contestants', models.ManyToManyField(blank=True, related_name='contestants', to='player.player')),
                ('first_victor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='player.player')),
            ],
        ),
    ]

# Generated by Django 4.2.4 on 2023-08-30 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('region', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('points', models.FloatField(default=0)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='region.region')),
            ],
        ),
    ]

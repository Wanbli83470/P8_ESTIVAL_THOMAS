# Generated by Django 2.1.7 on 2019-05-02 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('P8', '0005_delete_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='profil',
            name='genre',
            field=models.CharField(default='Homme', max_length=5),
        ),
    ]
# Generated by Django 2.1.7 on 2019-05-01 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('P8', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CATEGORIES',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NOM', models.CharField(max_length=80)),
                ('LINK_OFF', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='PRODUIT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NOM', models.CharField(max_length=200)),
                ('PRODUIT_URL', models.CharField(max_length=200)),
                ('STORE', models.CharField(max_length=50)),
                ('NUTRISCORE', models.IntegerField()),
                ('CATEGORIE_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='P8.CATEGORIES')),
            ],
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=ChildProcessError, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SUBSTITUT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NOM', models.CharField(max_length=200)),
                ('STORE', models.CharField(max_length=50)),
                ('SUBSTITUT_URL', models.CharField(max_length=200)),
                ('DESCRIPTION', models.TextField()),
            ],
        ),
    ]
# Generated by Django 2.1.7 on 2019-05-18 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('P8', '0007_auto_20190502_1741'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='substitut',
            name='DESCRIPTION',
        ),
        migrations.RemoveField(
            model_name='substitut',
            name='IMG_URL',
        ),
        migrations.RemoveField(
            model_name='substitut',
            name='NOM',
        ),
        migrations.RemoveField(
            model_name='substitut',
            name='STORE',
        ),
        migrations.RemoveField(
            model_name='substitut',
            name='SUBSTITUT_URL',
        ),
        migrations.AddField(
            model_name='substitut',
            name='PRODUIT_ID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='P8.PRODUIT'),
            preserve_default=False,
        ),
    ]
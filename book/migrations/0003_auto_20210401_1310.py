# Generated by Django 3.1.7 on 2021-04-01 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_leads'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leads',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
    ]
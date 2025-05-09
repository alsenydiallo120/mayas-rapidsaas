# Generated by Django 4.2.10 on 2024-10-12 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentications', '0004_customuser_site_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterUniqueTogether(
            name='customuser',
            unique_together={('email', 'site_name')},
        ),
    ]

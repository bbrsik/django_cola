# Generated by Django 4.2.7 on 2024-04-24 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_rename_birth_date_profile_birthdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='profiles/'),
        ),
    ]

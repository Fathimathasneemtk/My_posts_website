# Generated by Django 5.0.1 on 2024-02-03 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpdateProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('username', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=25)),
                ('image', models.ImageField(upload_to='media\\profiles')),
            ],
        ),
    ]

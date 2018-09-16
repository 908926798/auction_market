# Generated by Django 2.1.1 on 2018-09-16 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateChat',
            fields=[
                ('sourceName', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('targetName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.user')),
            ],
        ),
    ]
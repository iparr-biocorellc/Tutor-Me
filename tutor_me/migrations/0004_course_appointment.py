# Generated by Django 4.1.5 on 2023-04-10 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tutor_me', '0003_remove_course_user_delete_appointment_delete_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mnemonic', models.CharField(max_length=10, null=True)),
                ('number', models.CharField(max_length=4, null=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('end', models.DateTimeField(default=django.utils.timezone.now)),
                ('confirmed', models.BooleanField(default=False)),
                ('note', models.CharField(max_length=200, null=True)),
                ('availability', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tutor_me.availability')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tutor_me.course')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

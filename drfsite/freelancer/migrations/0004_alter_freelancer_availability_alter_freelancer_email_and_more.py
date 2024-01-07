# Generated by Django 4.2.7 on 2023-11-23 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0003_alter_freelancer_availability_alter_freelancer_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelancer',
            name='availability',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='freelancer',
            name='email',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='freelancer',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='freelancer',
            name='phone_number',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='freelancer',
            name='position',
            field=models.CharField(choices=[('Backend Developer', 'Be Developer'), ('Frontend Developer', 'Fe Developer'), ('DevOps', 'Devops')], max_length=255),
        ),
        migrations.AlterField(
            model_name='freelancer',
            name='salary',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
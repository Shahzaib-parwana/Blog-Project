# Generated by Django 5.0.3 on 2024-11-14 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_category_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogspost',
            name='blog_images',
            field=models.ImageField(blank=True, null=True, upload_to='blog_pictures/'),
        ),
    ]

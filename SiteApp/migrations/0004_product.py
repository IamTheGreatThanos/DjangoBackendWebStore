# Generated by Django 3.2.9 on 2021-12-13 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SiteApp', '0003_remove_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('image', models.CharField(max_length=255, verbose_name='https://tracerproducts.com/wp-content/uploads/2019/12/Product-Image-Coming-Soon.jpg')),
            ],
        ),
    ]

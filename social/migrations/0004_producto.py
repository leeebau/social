# Generated by Django 4.2.5 on 2023-11-22 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_auto_20201007_0744'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]

# Generated by Django 3.2.5 on 2022-06-22 12:24

import cart.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('cart', '0006_auto_20220622_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=cart.models.OrderItem),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.user'),
        ),
        migrations.RemoveField(
            model_name='OrderItem',
            name='item',
        ),
        migrations.AddField(
            model_name='OrderItem',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
    ]
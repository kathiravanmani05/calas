# Generated by Django 5.0.4 on 2024-06-05 03:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_image_name_alter_product_material_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='name',
        ),
        migrations.AlterUniqueTogether(
            name='productcategory',
            unique_together={('product_name', 'category')},
        ),
        migrations.AddField(
            model_name='productcategory',
            name='product_name',
            field=models.ForeignKey(db_column='product_name', default=None, on_delete=django.db.models.deletion.CASCADE, to='shop.product'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(related_name='products', to='shop.category'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='category',
            field=models.ForeignKey(db_column='category_id', on_delete=django.db.models.deletion.CASCADE, to='shop.category'),
        ),
        migrations.RemoveField(
            model_name='productcategory',
            name='product',
        ),
    ]
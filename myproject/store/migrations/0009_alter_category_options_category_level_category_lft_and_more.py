# Generated by Django 5.1.1 on 2024-11-01 07:58

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_producttags_product_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={},
        ),
        migrations.AddField(
            model_name='category',
            name='level',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='category',
            name='lft',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='category',
            name='rght',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='category',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='store.category'),
        ),
    ]

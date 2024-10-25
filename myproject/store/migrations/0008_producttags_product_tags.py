# Generated by Django 5.1.1 on 2024-10-25 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_product_validate_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(related_name='product_tags', to='store.producttags'),
        ),
    ]
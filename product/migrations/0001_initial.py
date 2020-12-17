# Generated by Django 3.1.4 on 2020-12-16 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='DeliveryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'delivery_types',
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'db_table': 'discounts',
            },
        ),
        migrations.CreateModel(
            name='Origin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'origins',
            },
        ),
        migrations.CreateModel(
            name='PackingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('packing_type', models.CharField(max_length=45)),
                ('cart_packing_type', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'packing_types',
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.category')),
            ],
            options={
                'db_table': 'subcategories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('subtitle', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sales_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('allergy', models.CharField(max_length=500)),
                ('expiration_date', models.DateField()),
                ('notice', models.CharField(max_length=200, null=True)),
                ('is_soldout', models.BooleanField(default=False)),
                ('image_url', models.URLField(max_length=2000)),
                ('delivery_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='product.deliverytype')),
                ('discount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='product.discount')),
                ('origin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='product.origin')),
                ('packing_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='product.packingtype')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.subcategory')),
            ],
            options={
                'db_table': 'products',
            },
        ),
    ]

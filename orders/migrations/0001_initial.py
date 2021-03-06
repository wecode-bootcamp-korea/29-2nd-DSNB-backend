# Generated by Django 4.0.2 on 2022-02-16 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'order_statuses',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'payment_methods',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ordered_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('link_url', models.CharField(max_length=250)),
                ('bookoption_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.bookoption')),
                ('order_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orderstatus')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='orders.paymentmethod')),
                ('target_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_user', to='users.user')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='origin_user', to='users.user')),
            ],
            options={
                'db_table': 'orders',
            },
        ),
    ]

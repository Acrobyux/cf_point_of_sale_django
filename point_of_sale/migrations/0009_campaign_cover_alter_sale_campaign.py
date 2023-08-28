# Generated by Django 4.2 on 2023-04-30 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('point_of_sale', '0008_rename_campaign_id_sale_campaign'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='cover',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Cuota de entrada al bazar', max_digits=8),
        ),
        migrations.AlterField(
            model_name='sale',
            name='campaign',
            field=models.ForeignKey(help_text='Producto vendido', on_delete=django.db.models.deletion.CASCADE, to='point_of_sale.campaign'),
        ),
    ]
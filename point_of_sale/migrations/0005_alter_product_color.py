# Generated by Django 4.2 on 2023-04-28 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("point_of_sale", "0004_alter_product_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="color",
            field=models.CharField(
                choices=[
                    ("UVA", "UVA"),
                    ("PIZARRA", "PIZARRA"),
                    ("BLANCO", "BLANCO"),
                    ("LILA ", "LILA "),
                    ("VINO", "VINO"),
                    ("CAFE", "CAFE"),
                    ("NEGRO", "NEGRO"),
                    ("FUCSIA", "FUCSIA"),
                    ("MOCCA ", "MOCCA "),
                    ("BEIGE", "BEIGE"),
                    ("CEREZA", "CEREZA"),
                    ("ARENA", "ARENA"),
                    ("AZUL REY", "AZUL REY"),
                    ("SHEDRON ", "SHEDRON "),
                    ("OXFORD", "OXFORD"),
                    ("NEGRO CON FLORES ", "NEGRO CON FLORES "),
                    ("BLANCO CON FLORES", "BLANCO CON FLORES"),
                    ("BLANCO CON FLORES ROJAS", "BLANCO CON FLORES ROJAS"),
                    ("BLANCO CON FLORES ROSAS ", "BLANCO CON FLORES ROSAS "),
                    ("ROJO CON FLORES FUERTE", "ROJO CON FLORES FUERTE"),
                    (
                        "ROJO CON FLORES BLANCAS CON VERDE ",
                        "ROJO CON FLORES BLANCAS CON VERDE ",
                    ),
                ],
                default=None,
                help_text="Color del producto",
                max_length=50,
            ),
        ),
    ]

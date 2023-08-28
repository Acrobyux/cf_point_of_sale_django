import datetime
from unittest import TestCase

from django.utils import timezone
from .models import Campaign


class CampaignModelTest(TestCase):

    def test_create_campaign_with_timezone(self):
        # Crear un objeto datetime con la fecha y hora deseada
        dt = datetime.datetime(2023, 8, 27, 18, 0, 0, 0)

        # Convertir el objeto datetime en un objeto aware de Django (con zona horaria)
        aware_dt = timezone.make_aware(dt, timezone.get_current_timezone())

        # Formatear la cadena de fecha y hora en el formato especificado
        formatted_dt = aware_dt.strftime('%Y-%m-%d %H:%M:%S.%f')

        # Crear una instancia de Campaign y guardarla en la base de datos
        campaign = Campaign.objects.create(
            name="Campaña de prueba",
            place="Lugar de la campaña",
            address="Dirección de la campaña",
            start_date=aware_dt,
            end_date=aware_dt,
            cover=100,
            is_active=True,
        )

        self.assertEqual(campaign.name, "Campaña de prueba")
        self.assertEqual(campaign.place, "Lugar de la campaña")
        self.assertEqual(campaign.address, "Dirección de la campaña")
        self.assertEqual(campaign.start_date.strftime('%Y-%m-%d %H:%M:%S.%f'), "2023-08-27 18:00:00.000000")
        self.assertEqual(campaign.end_date.strftime('%Y-%m-%d %H:%M:%S.%f'), "2023-08-27 18:00:00.000000")
        self.assertEqual(campaign.cover, 100)
        self.assertEqual(campaign.is_active, True)

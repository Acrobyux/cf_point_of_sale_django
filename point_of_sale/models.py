import threading
from io import BytesIO
from time import sleep

from PIL import Image
from django.db import models
import base64

from .constants import DEFAULT_PRODUCT_IMAGE, SIZE_CHOICES, COLOR_CHOICES
from .mailers import NewCampaignMailer


class Category(models.Model):
    """
        Model representing a product category.
        Each category can be associated with multiple products, forming a one-to-many relationship.
    """
    name = models.CharField(max_length=100, help_text="Nombre de la categoría")
    is_active = models.BooleanField(
        default=True, help_text="Indica si la categoría está activa o no"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Fecha de creación de la categoría"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Fecha de la última actualización de la categoría"
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    """
        Model representing a product category.
        Each product belongs to a specific category, forming a many-to-one relationship.
        Each product can be associated with multiple sales, forming a one-to-many relationship.
    """
    name = models.CharField(max_length=100, help_text="Nombre del producto")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        help_text="Categoría a la que pertenece el producto"
    )
    inventory_quantity = models.IntegerField(
        default=0, help_text="Cantidad en inventario del producto"
    )
    buy_price = models.DecimalField(
        max_digits=8, decimal_places=2,
        help_text="Precio de compra del producto"
    )
    sold_price = models.DecimalField(
        max_digits=8, decimal_places=2,
        help_text="Precio de venta del producto"
    )
    image = models.ImageField(
        upload_to='product_images', null=True, blank=True,
        help_text="Imagen del producto"
    )
    size = models.CharField(
        max_length=2, choices=SIZE_CHOICES,
        help_text="Talla del producto", default=None
    )
    color = models.CharField(
        max_length=50, choices=COLOR_CHOICES,
        help_text="Color del producto", default=None
    )
    is_active = models.BooleanField(
        default=True, help_text="Indica si el producto está activo o no"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Fecha de creación del producto"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Fecha de la última actualización del producto"
    )

    def __str__(self):
        return f"{self.name}/{self.color}/{self.size}"

    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "category": self.category.name,
            "inventory_quantity": self.inventory_quantity,
            "buy_price": self.buy_price,
            "sold_price": self.sold_price,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "size": self.size,
            "color": self.color,
        }

        url = self.image if self.image else DEFAULT_PRODUCT_IMAGE

        with BytesIO() as buffer:
            image = Image.open(url)
            # Convierte la imagen a modo RGB
            image = image.convert("RGB")
            image.save(buffer, format="JPEG")
            data["image"] = base64.b64encode(buffer.getvalue()).decode()

        return data

    def get_image_as_base64(self):
        url = self.image if self.image else DEFAULT_PRODUCT_IMAGE

        with BytesIO() as buffer:
            image = Image.open(url)
            # Convierte la imagen a modo RGB
            image = image.convert("RGB")
            image.save(buffer, format="JPEG")
            return base64.b64encode(buffer.getvalue()).decode()

    @classmethod
    def get_product_by_id(cls, product_id):
        return cls.objects.get(id=product_id)


class Campaign(models.Model):
    name = models.CharField(max_length=100, help_text="Nombre de la campaña")
    place = models.CharField(max_length=100, help_text="Lugar de la campaña")
    address = models.CharField(
        max_length=100,
        help_text="Dirección de la campaña"
    )
    image = models.ImageField(
        upload_to='campaign_images', null=True, blank=True,
        help_text="Imagen de la campaña"
    )
    start_date = models.DateTimeField(
        help_text="Fecha de inicio de la campaña"
    )
    end_date = models.DateTimeField(
        help_text="Fecha de fin de la campaña"
    )
    cover = models.DecimalField(
        default=0, max_digits=8, decimal_places=2,
        help_text="Cuota de entrada al bazar"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indica si la campaña está activa o no"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación de la campaña"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Fecha de la última actualización de la campaña"
    )

    def __str__(self):
        return self.name

    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "place": self.place,
            "address": self.address,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

        return data

    def get_image_as_base64(self):
        url = self.image if self.image else DEFAULT_PRODUCT_IMAGE

        with BytesIO() as buffer:
            image = Image.open(url)
            # Convierte la imagen a modo RGB
            image = image.convert("RGB")
            image.save(buffer, format="JPEG")
            return base64.b64encode(buffer.getvalue()).decode()

    def set_previous_inactive(self):
        """ Deactivates all previous campaigns """
        Campaign.objects.all().update(is_active=False)

    def notify_about_new_campaign(self):
        """
        Notify via Email all previous clients
        about the new campaign
        """
        try:
            # Verify if there are sales with an email registered
            mails = Sale.get_clients_email()

            if mails:
                mailer = NewCampaignMailer()
                mail = mailer.create_mail(
                    f'Visitanos en el Bazar {self.name}',
                    'mails/new_campaign.html',
                    self.to_dict(),
                    mails
                )

                if self.image:
                    mail.attach_file(self.image.path, self.image.name)

                thread = threading.Thread(target=mailer.send_mail, args=(mail,))
                thread.start()
        except Exception as e:
            print(f"Ocurrio un error al notificar a los clientes. Error: {e}")

    def save(self, *args, **kwargs):
        """
        Deactivates all previous campaigns
        before saving the new campaign
        and notifies all clients about
        the new campaign via Email
        """
        self.set_previous_inactive()
        super().save(*args, **kwargs)
        self.notify_about_new_campaign()


class Sale(models.Model):
    user_id = models.IntegerField(
        default=0, help_text="ID del usuario que realizó la venta"
    )
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, help_text="Producto vendido"
    )
    date = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora en la que se realizó la venta"
    )
    change = models.DecimalField(
        max_digits=8, decimal_places=2,
        help_text="Cambio dado al cliente"
    )
    payment = models.DecimalField(
        max_digits=8, decimal_places=2,
        help_text="Pago recibido del cliente"
    )
    gain = models.DecimalField(
        max_digits=8, decimal_places=2,
        help_text="Ganancia total de la venta"
    )
    amount = models.DecimalField(
        max_digits=8, decimal_places=2,
        help_text="Monto total de la venta"
    )
    products = models.IntegerField(
        help_text="Cantidad de productos vendidos"
    )
    client_email = models.EmailField(
        null=True, blank=True,
        help_text="Correo electrónico del cliente"
    )

    def __str__(self):
        return (
            f"Venta #{self.id} realizada por usuario #{self.user_id} "
            f"el {self.date}. Ganancia: {self.gain}"
        )

    def get_folio(self):
        folio = str(self.id)
        return "#{:0>3}".format(folio)

    def to_dict(self):
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "date": self.date,
            "change": self.change,
            "payment": self.payment,
            "gain": self.gain,
            "amount": self.amount,
            "products": self.products,
            "items": [
                {
                    "product": sale_item.product.name,
                    "quantity": sale_item.quantity,
                    "price": sale_item.price,
                    "gain": sale_item.gain,
                }
                for sale_item in self.saleitem_set.all()
            ],
        }
        return data

    @classmethod
    def get_sale_by_id(cls, sale_id):
        return cls.objects.get(id=sale_id)

    @classmethod
    def get_clients_email(cls):
        return {
            client.client_email for client
            in cls.objects.all() if client.client_email
        }


class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale, on_delete=models.CASCADE,
        help_text="Venta a la que pertenece el item"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        help_text="Producto vendido"
    )
    quantity = models.IntegerField(
        default=0,
        help_text="Cantidad vendida del producto"
    )
    price = models.DecimalField(
        max_digits=8, decimal_places=2,
        help_text="Precio al que se vendió el producto"
    )
    gain = models.DecimalField(
        max_digits=8, decimal_places=2,
        help_text="Ganancia de la venta del producto"
    )

    def __str__(self):
        return f"{self.product.name} ({self.quantity} x {self.price})"

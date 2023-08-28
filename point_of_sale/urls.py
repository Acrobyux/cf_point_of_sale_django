from django.urls import path
from . import views

app_name = 'point_of_sale'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'sale/<int:sale_id>/',
        views.sale_detail,
        name='sale_detail'
    ),
    path(
        'categories/',
        views.categories,
        name='categories'
    ),
    path(
        'category/<int:category_id>/products/',
        views.products_by_category,
        name='products_by_category'
    ),
    path(
        'products/',
        views.products,
        name='products'
    ),
    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),
    path(
        'new-sale/',
        views.new_sale,
        name='new_sale'
    ),
    path(
        'get-product/<int:product_id>',
        views.get_product,
        name='get_product'
    ),
    path(
        'get_product_suggestions/',
        views.get_product_suggestions,
        name='get_product_suggestions'
    ),
    path(
        'campaigns/',
        views.campaigns,
        name='campaigns'
    ),
    path(
        'campaign/<int:campaign_id>',
        views.campaign_detail,
        name='campaign_detail'
    ),
    path(
        'end_campaign/<int:campaign_id>',
        views.end_campaign,
        name='end_campaign'
    ),
    path(
        'get_client_email_suggestions/',
        views.get_client_email_suggestions,
        name='get_client_email_suggestions'
    ),
]

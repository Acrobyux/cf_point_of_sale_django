import json
import time
import threading
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render

from point_of_sale.models import Sale, Product, SaleItem, Category, Campaign
from point_of_sale.mailers import NewCampaignMailer


# Create your views here.

@login_required
def index(request):
    campaign_id = int(request.GET.get('campaign', -1))
    campaigns = Campaign.objects.all().order_by('-id')

    try:
        current_campaign = Campaign.objects.filter(is_active=True).get()
    except Campaign.DoesNotExist:
        current_campaign = None
        campaign_id = -1
    sales = Sale.objects.filter(campaign_id=campaign_id).order_by(
        '-id') if campaign_id > 0 else Sale.objects.all().order_by('-id')
    total_gain, total_items, cover = 0, 0, 1
    total_inventory = (
            Product.objects
            .filter(is_active=True)
            .aggregate(Sum('inventory_quantity'))['inventory_quantity__sum']
            or 0
    )

    for sale in sales:
        sale.user = User.objects.get(id=sale.user_id)
        total_gain += sale.gain
        total_items += sale.saleitem_set.count()
    if current_campaign:
        cover = current_campaign.cover or 1
    else:
        cover = 1

    progress = round((total_gain / cover) * 100, 2)

    return render(request, 'index.html', {
        'campaigns': campaigns,
        'current_campaign': current_campaign,
        'campaign_id': campaign_id,
        'sales': sales,
        'total_gain': total_gain,
        'total_items': total_items,
        'total_inventory': total_inventory,
        'cover': cover,
        'progress': progress
    })


@login_required
def sale_detail(request, sale_id):
    sale = Sale.get_sale_by_id(sale_id)
    return render(request, 'sale_detail.html', {'sale': sale})


@login_required
def product_detail(request, product_id):
    product = Product.get_product_by_id(product_id)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def new_sale(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_change, user_payment = data['change'], data['payment']
        client_email = data['client_email']
        user_id = request.user.id
        cart = data['cart']
        gain, amount, products_quantity = 0, 0, 0
        products = []
        for item in cart:
            product = Product.objects.get(id=item['product_id'])
            item_quantity = Decimal(item['quantity'])
            item_price = Decimal(item['price'])
            product_buy_price = Decimal(product.buy_price)
            gain += (Decimal(item['price']) * Decimal(item['quantity'])) - (
                    Decimal(product.buy_price) * Decimal(item['quantity']))
            amount += (Decimal(item['price']) * Decimal(item['quantity']))
            products_quantity += int(item['quantity'])
            products.append({
                'product_id': product.id,
                'quantity': item['quantity'],
                'price': item['price'],
                'gain': (item_price * item_quantity) -
                        (product_buy_price * item_quantity),
                'amount': item_price * item_quantity,
            })

        current_campaign = Campaign.objects.filter(is_active=True).first()
        sale = Sale.objects.create(
            user_id=user_id, change=user_change, payment=user_payment,
            gain=gain, amount=amount, products=products_quantity,
            campaign_id=current_campaign.id, client_email=client_email
        )

        if sale:
            for item in products:
                product = Product.objects.get(id=item['product_id'])
                product.inventory_quantity -= int(item['quantity'])
                product.save()
                SaleItem.objects.create(
                    sale=sale, product=product, quantity=item['quantity'],
                    price=item['amount'], gain=item['gain']
                )
            return JsonResponse({'success': True, 'data': sale.to_dict()})
        else:
            return JsonResponse(
                {'success': False,
                 'message': 'Error al guardar la venta'}
            )
    elif request.method == 'GET':
        # mostrar formulario
        return render(request, 'new_sale.html')


@login_required
def get_product(request: HttpRequest, product_id: int) -> JsonResponse:
    """Gets a product detail by a given id.

    Args:
        request (HttpRequest): The received HTTP request.
        product_id (int): The ID of the product to be fetched.

    Returns:
        JsonResponse: A JSON Response with product's
        details or an error message.

    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse(
            {'success': False,
             'message': 'Producto no encontrado'}
        )

    if product.is_active:
        if product.inventory_quantity > 0:
            return JsonResponse(
                {'success': True,
                 'product': product.to_dict()}
            )
        else:
            return JsonResponse(
                {'success': False,
                 'message': 'Producto sin stock'}
            )
    else:
        return JsonResponse(
            {'success': False,
             'message': 'Producto no disponible'}
        )


@login_required
def categories(request):
    return render(
        request,
        'categories.html',
        {'categories': Category.objects.all()}
    )


@login_required
def products(request):
    products = Product.objects.all()
    return render(
        request,
        'products.html',
        {'products': products}
    )


@login_required
def products_by_category(request, category_id):
    category = Category.objects.get(id=category_id)
    return render(
        request,
        'products_by_category.html',
        {'products': category.product_set.filter(is_active=True),
         'category': category}
    )


@login_required
def products(request):
    return render(
        request,
        'products.html',
        {'products': Product.objects.filter(is_active=True)}
    )


@login_required
def campaigns(request):
    campaigns = Campaign.objects.all().order_by('-id')
    for campaign in campaigns:
        campaign.gain = (
                campaign.
                sale_set.
                aggregate(Sum('gain'))['gain__sum']
                or 0
        )
        campaign.net_gain = campaign.gain - campaign.cover
    return render(
        request,
        'campaigns.html',
        {'campaigns': campaigns}
    )


@login_required
def campaign_detail(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    sales = campaign.sale_set.all()
    products_sold_count, brute_gain, gross_gain = 0, 0, 0
    if sales:
        products_sold_count = (
            sales
            .aggregate(products_sum=Sum('products'))['products_sum']
        )
        brute_gain = sales.aggregate(gain_sum=Sum('gain'))['gain_sum']
        gross_gain = brute_gain - campaign.cover
    campaign.brute_gain = brute_gain
    campaign.gross_gain = gross_gain
    return render(
        request,
        'campaign_detail.html',
        {'campaign': campaign,
         'products_sold_count': products_sold_count}
    )


@login_required
def end_campaign(request: HttpRequest, campaign_id: int) -> JsonResponse:
    try:
        campaign = Campaign.objects.get(id=campaign_id)
        campaign.is_active = False
        campaign.save()
    except Campaign.DoesNotExist:
        return JsonResponse(
            {
                "success": False,
                "message": "No se encontro la Campana"
            }
        )

    return JsonResponse(
        {
            "Success": True,
            "message": "Se ha finalizado la campana",
            "campaign": campaign.to_dict()
        }
    )


@login_required
def get_client_email_suggestions(request: HttpRequest) -> JsonResponse:
    """
        Retrieves email suggestions based on user input.

        Args:
            request (HttpRequest):
                The HTTP request object containing user data.

        Returns:
            JsonResponse: A JSON response containing
            a list of unique email suggestions.

        Example:
            If the user enters 'leo' in the input field,
            and there are email addresses in the database like
            'leo@example.com' and 'leo_messi@gmail.com',
            the response will be:
            {
                "emails": ["leo@example.com", "leo_messi@gmail.com"]
            }
        """

    q = request.GET.get("q", "")
    emails = {
        sale.client_email for sale
        in
        Sale.objects.filter(client_email__icontains=q)
    }

    return JsonResponse({"emails": list(emails)})


@login_required
def get_product_suggestions(request: HttpRequest) -> JsonResponse:
    """
        Retrieves product suggestions based on user input.

        Args:
            request (HttpRequest):
                The HTTP request object containing user data.

        Returns:
            JsonResponse:
                A JSON response containing a
                list of unique product suggestions.

        Example:
            If the user enters 'leo' in the input field,
            and there are email addresses in the database like
            'leo@example.com' and 'leo_messi@gmail.com',
            the response will be:
            {
                "emails": ["leo@example.com", "leo_messi@gmail.com"]
            }
        """

    q = request.GET.get("q", "")
    products_list = [
        product.to_dict() for product
        in
        Product.objects.filter(name__icontains=q)
    ]

    return JsonResponse({"products": list(products_list)})

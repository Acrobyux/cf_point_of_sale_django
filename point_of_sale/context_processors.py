from datetime import datetime
from point_of_sale.models import Product, Category, Sale


def global_counts(request):
    """Add global counts to the context."""
    return {
        'product_count': Product.objects.filter(is_active=True).count(),
        'category_count': Category.objects.filter(is_active=True).count(),
        'sales_count': Sale.objects.count(),
        'now': datetime.now(),
    }

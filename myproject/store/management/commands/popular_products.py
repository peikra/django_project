from django.core.management import BaseCommand
from django.db.models import Count
from store.models import Product


class Command(BaseCommand):
    help = "Finds the top 3 most popular products"


    def handle(self, *args, **options):
        popular_products = (
            Product.objects
            .annotate(user_count=Count('cartitem__cart__user', distinct=True))
            .order_by('-user_count')[:3]
        )

        if popular_products:
            self.stdout.write("Top 3 Most Popular Products:")
            for rank, product in enumerate(popular_products, start=1):
                self.stdout.write(f"{rank}. {product.name} - {product.user_count} users")
        else:
            self.stdout.write("No products found.")
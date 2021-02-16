from import_export import resources
from .models import OrderLine

class OrderResource(resources.ModelResource):
    class Meta:
        model = OrderLine
        fields = ('order__department__number', 'inventory__inventory_text', 'qty', 'unit', 'line_cost', )
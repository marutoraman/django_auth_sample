from rest_framework import viewsets

from ..models import ItemModel
from ..serializers.item import ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = ItemModel.objects.all()
    serializer_class = ItemSerializer
    filter_fields = ('name',) 
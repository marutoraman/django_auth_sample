from rest_framework import viewsets

from ..models import UserFavoriteItemModel
from ..serializers.user_favorite_item import UserFavoriteItemSerializer


class UserFavoriteItemViewSet(viewsets.ModelViewSet):
    queryset = UserFavoriteItemModel.objects.all()
    serializer_class = UserFavoriteItemSerializer
    filter_fields = ('name',) 
from django.urls import path, include
from rest_framework import routers


# from .serializers.item import ItemSerializer
from .view_sets.item import ItemViewSet
from .views.dashboard import DashboardView
from .views.item import ItemView
from .views.api.user_favorite_item import UserFavoriteItemAPIView

app_name = "my_app"
urlpatterns = [
    path('dashboard', DashboardView.as_view(), name="dashboard"),
    path('item', ItemView.as_view(), name="item"),
    path(r'api/item_favorite', UserFavoriteItemAPIView.as_view())
]

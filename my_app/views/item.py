from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import TemplateView
from ..models import ItemModel, UserFavoriteItemModel

app_name = "my_app"

class ItemView(TemplateView):
    template_name = f"{app_name}/item.html"
    
    def get(self, request):
        items = ItemModel.objects.all()
        favorite_items = UserFavoriteItemModel.objects.filter(user=request.user).all()
        for item in items:
            item.is_favorited = False
            for favorite_item in favorite_items:
                if item.id == favorite_item.item_id:
                    item.is_favorited = True
                    break
        return self.render_to_response({"items": items})
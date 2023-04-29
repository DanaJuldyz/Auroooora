from django.core.cache import cache
from django.db.models import Count

from service.models import *

menu = [{ 'title': "About Site", 'url_name': 'about'},
        { 'title': "Add Product", 'url_name': 'create'},
        { 'title': "Contact Us", 'url_name': 'contact'},
]

class DataMixin:
    paginate_by = 8
    def get_user_context(self,**kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.all()
            cache.set('cats', cats, 60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = cats
        return context
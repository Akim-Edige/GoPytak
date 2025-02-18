from django.urls import path
from orders import views as orders_views

app_name = 'orders'
urlpatterns = [
    path('', orders_views.IndexView.as_view(), name='index' ),
    path('create/', orders_views.OrderCreateView.as_view(), name='create_order' ),

    path('get-subcategories/', orders_views.GetSubcategoriesView.as_view(), name='get_subcategories'),
    path('get-services/', orders_views.GetServicesView.as_view(), name='get_services'),
]

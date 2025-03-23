from django.urls import path
from orders import views as orders_views

app_name = 'orders'
urlpatterns = [
    path('', orders_views.IndexView.as_view(), name='index' ),
    path('create/', orders_views.OrderCreateView.as_view(), name='create_order' ),

    path('get-subcategories/', orders_views.GetSubcategoriesView.as_view(), name='get_subcategories'),
    path('get-services/', orders_views.GetServicesView.as_view(), name='get_services'),
    path('bargain/room/<chatroom_name>', orders_views.chat_view, name="chatroom"),

    path('accept-offer/<offer_id>', orders_views.accept_offer, name="accept-offer"),
    path('order/<str:order_id>/', orders_views.OrderDetailView.as_view(), name='order_detail'),

    path('myorders/', orders_views.user_orders, name='user_orders'),
]

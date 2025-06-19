from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, MenuItemViewSet, OrderViewSet, OrderItemViewSet
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),  # Homepage
]

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
urlpatterns = router.urls
urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('cart/', views.view_cart, name='view-cart'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add-to-cart'),
    path('place-order/', views.place_order, name='place-order'),
]

urlpatterns += [
    path('', views.home_view, name='home'),
    path('restaurants/', views.restaurant_list, name='restaurant-list'),
    path('restaurant/<int:restaurant_id>/', views.menu_items_view, name='restaurant-menu'),
    path('orders/', views.order_history, name='order-history'),
    path('admin-panel/orders/', views.manage_orders, name='manage-orders'),
    path('admin-panel/order/<int:order_id>/update/', views.update_order_status, name='update-order-status'),
]
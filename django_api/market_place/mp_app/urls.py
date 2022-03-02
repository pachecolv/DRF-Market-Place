from django.urls import path

from . import views

urlpatterns = [
	path('signup/', views.SignUp.as_view(), name='sign-up'),
	path('seller/', views.SellerDetail.as_view(), name='seller-detail'),
	path('products/', views.ProductsList.as_view(), name='products-list'),
	path('product/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
	path('product/<int:pk>/buy/', views.BuyProduct.as_view(), name='buy-product'),
]
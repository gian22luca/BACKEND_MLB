from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.inicio , name='inicio' ),
    path('info/', views.api_info),
    path('usuarios/', views.UsuarioAPIView.as_view()),
    path('productos/', views.ProductoAPIView.as_view()),
    path('pedidos/', views.PedidoAPIView.as_view()),
    path('usuarios/<int:pk>/', views.UsuarioDetalleAPIView.as_view()),
    path('productos/<int:pk>/', views.ProductoDetalleAPIView.as_view()),
    path('pedidos/<int:pk>/', views.PedidoDetalleAPIView.as_view()),
 
]
 
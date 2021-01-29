from django.urls import path, re_path, include

from . import views 
app_name = "prestamo_app"

urlpatterns = [
    path('', views.InicioView.as_view(), name="home"),
    path('listaPrestamos/', views.PrestamosListView.as_view(), name="listaPrestamos"),
    path('agregarPrestamos/', views.PrestamosCreateView.as_view(), name="agregarPrestamos"),
    path('detallePrestamos/<pk>', views.PrestamosDetailView.as_view(), name="detallePrestamos"),
    path('editarPrestamos/<pk>', views.PrestamosUpdateView.as_view(), name="editarPrestamos"),
    path('eliminarPrestamos/<pk>', views.PrestamosDeleteView.as_view(), name="eliminarPrestamos"),
]

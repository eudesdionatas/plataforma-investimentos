from django.urls import path
from . import views

urlpatterns = [
    path('cadastro-operacao/', views.cadastro_operacao, name='cadastro_operacao'),
]
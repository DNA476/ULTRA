from django.urls import path

from .views import (
    ModelCardCreateView,
    ModelCardDeleteView,
    ModelCardDetailView,
    ModelCardListView,
    ModelCardUpdateView,
)

app_name = 'models_app'

urlpatterns = [
    path('', ModelCardListView.as_view(), name='model_list'),
    path('create/', ModelCardCreateView.as_view(), name='model_create'),
    path('<int:pk>/', ModelCardDetailView.as_view(), name='model_detail'),
    path('<int:pk>/edit/', ModelCardUpdateView.as_view(), name='model_update'),
    path('<int:pk>/delete/', ModelCardDeleteView.as_view(), name='model_delete'),
]

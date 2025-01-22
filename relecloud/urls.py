## APP (relecloud)
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('destinations/', views.destinations, name='destinations'),
    path('cruises/', views.cruises, name='cruises'),
    path('destination/<int:pk>/', views.DestinationDetailView.as_view(), name='destination_detail'),
    path('cruise/<int:pk>/', views.CruiseDetailView.as_view(), name='cruise_detail'),
    path('info_request/', views.InfoRequestCreate.as_view(), name='info_request'),
    path('reviews/', views.reviews, name='reviews'),

    # CRUD for Destinations
    path('destination/create/', views.DestinationCreateView.as_view(), name='destination_create'),
    path('destination/<int:pk>/edit/', views.DestinationUpdateView.as_view(), name='destination_edit'),
    path('destination/<int:pk>/delete/', views.DestinationDeleteView.as_view(), name='destination_delete'),

     # CRUD for Cruises
    path('cruise/create/', views.CruiseCreateView.as_view(), name='cruise_create'),
    path('cruise/<int:pk>/edit/', views.CruiseUpdateView.as_view(), name='cruise_edit'),
    path('cruise/<int:pk>/delete/', views.CruiseDeleteView.as_view(), name='cruise_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

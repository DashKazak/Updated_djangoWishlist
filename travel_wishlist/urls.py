from django.urls import path
from . import views

urlpatterns = [
    path('', views.place_list,name='place_list'),
    # path('about', views.about, name='about'),
    path('visited',views.places_visited, name='places_visited'),
    #placeholder
    #will match requests from the database with the url
    path('place/<int:place_pk>/was_visited/',views.place_was_visited,name='place_was_visited'),
    #capturing
    path('place/<int:place_pk>', views.place_details, name = 'place_details'),
    path('place/<int:place_pk>/delete', views.delete_place, name = 'delete_place')
    #name is used for url reversing in the templates
]
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inscription/', views.signup.as_view(), name='signup'),
    path('Annonce/ajouter/', views.ajouterAnnonce, name='ajouterAnnonce'),
    path('Estimation/', views.Estimation, name='Estimation'),
    path('Annonce/', views.consulterAnnonce, name='consulterAnnonce'),
    path('Annonce/supprimer/<int:id>/', views.supprimerAnnonce, name='supprimerAnnonce'),
    path('Annonce/modifier/<int:id>/', views.modifierAnnonce, name='modifierAnnonce'),
    path('Annonce/<int:id>/', views.afficherAnnonce, name='afficherAnnonce'),
]
from django.db import models
    
class Personne_physique(models.Model):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    telephone = models.IntegerField(default=0)
    adresse = models.CharField(max_length=60)
    email = models.EmailField()
    identifiant = models.CharField(max_length=60, default="")
    
class Annonce(models.Model):
  titre = models.CharField(max_length=200)
  description = models.CharField(max_length=200)
  image = models.ImageField(upload_to = 'gallerie/', default = 'default_car.jpg')
  datePublication = models.DateTimeField('datePublication')
  marque = models.CharField(max_length=60)
  modele = models.CharField(max_length=60)
  boiteVitesse = models.CharField(max_length=30)
  puissanceFiscale = models.IntegerField(default=0)
  energie = models.CharField(max_length=60)
  kilometrage = models.IntegerField(default=0)
  prix = models.FloatField(default=0)
  personne = models.CharField(max_length=30)

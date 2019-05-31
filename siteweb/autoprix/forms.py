import datetime

from django import forms

class AnnonceFrm(forms.Form):
  titre = forms.CharField(label='titre', max_length=200, required=True)
  description = forms.CharField(label='description', widget=forms.Textarea, max_length=1000, required=True)
  #image = forms.ImageField(label='Image')
  marque = forms.CharField(label='marque', max_length=60, required=True)
  modele = forms.CharField(label='modele', max_length=60, required=True)
  boiteVitesse = forms.CharField(label='boiteVitesse', max_length=30, required=True)
  puissanceFiscale = forms.IntegerField(label='puissanceFiscale', required=True)
  energie = forms.CharField(label='energie', max_length=60, required=True)
  kilometrage = forms.IntegerField(label='kilometrage', required=True)
  prix = forms.FloatField(label='prix', required=True)
     
ENERGY_CHOICES = (
    (0, _("essence")),
    (1, _("diesel"))
)
BV_CHOICES = (
    (0, _("mécanique")),
    (1, _("automatique")),
    (2, _("manuelle"))
)
class FormPrix(forms.Form):
    kilometrage = forms.IntegerField(required=True)
    annee = forms.IntegerField(required=True)
    energie = forms.ChoiceField(choices = ENERGY_CHOICES, required=True)
    boite = forms.ChoiceField(choices = BV_CHOICES, required=True)
    puissance = forms.IntegerField(required=True)

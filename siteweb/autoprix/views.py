import datetime
import csv

from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from .models import Annonce
from .forms import AnnonceFrm, FormPrix
from sklearn.externals import joblib

class signup(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'inscription.html'

def index(request):
    #if request.user.is_authentificated():
    #    return consulterAnnonces()
    #else:
    return render(request, 'index.html', {})
        
def ajouterAnnonce(request):
    form_data=AnnonceFrm(request.POST or None)
    msg=''
    if form_data.is_valid():
        nouveau_Annonce=Annonce()
        nouveau_Annonce.titre = form_data.cleaned_data['titre']
        nouveau_Annonce.description = form_data.cleaned_data['description']
        #nouveau_Annonce.image = form_data.cleaned_data['image']
        nouveau_Annonce.datePublication = datetime.datetime.now()
        nouveau_Annonce.marque = form_data.cleaned_data['marque']
        nouveau_Annonce.modele = form_data.cleaned_data['modele']
        nouveau_Annonce.boiteVitesse = form_data.cleaned_data['boiteVitesse']
        nouveau_Annonce.puissanceFiscale = form_data.cleaned_data['puissanceFiscale']
        nouveau_Annonce.energie = form_data.cleaned_data['energie']
        nouveau_Annonce.kilometrage = form_data.cleaned_data['kilometrage']
        nouveau_Annonce.prix = form_data.cleaned_data['prix']
        nouveau_Annonce.personne = request.user.username
        nouveau_Annonce.save()
        msg='Annonce a été ajouté avec succès'
    context={
        'form':form_data,
        'msg':msg
    }

    return render(request,'ajouterAnnonce.html',context)

def consulterAnnonce(request):
    liste_Annonce = Annonce.objects.all()
    context={
        'Annonces':liste_Annonce    }
    return render(request,'consulterAnnonce.html',context)

def supprimerAnnonce(request, id):
    supprimer_Annonce = Annonce.objects.filter(pk=id)[0]
    supprimer_Annonce.delete()
    return render(request,'supprimerAnnonce.html',{})

def modifierAnnonce(request, id):
    ancien_Annonce = Annonce.objects.filter(pk=id)[0]
    form_data=AnnonceFrm(request.POST or None,
        initial={

                  'titre' : ancien_Annonce.titre,
                  'description' : ancien_Annonce.description,
                  'datePublication' : ancien_Annonce.datePublication,
                  'marque' : ancien_Annonce.marque,
                  'modele' : ancien_Annonce.modele,
                  'boiteVitesse' : ancien_Annonce.boiteVitesse,
                  'puissanceFiscale' : ancien_Annonce.puissanceFiscale,
                  'energie' : ancien_Annonce.energie,
                  'kilometrage' : ancien_Annonce.kilometrage,
                  'prix' : ancien_Annonce.prix
        }
    )
    msg=''
    if form_data.is_valid():
        ancien_Annonce.titre = form_data.cleaned_data['titre']
        ancien_Annonce.description = form_data.cleaned_data['description']
        ancien_Annonce.marque = form_data.cleaned_data['marque']
        ancien_Annonce.modele = form_data.cleaned_data['modele']
        ancien_Annonce.boiteVitesse = form_data.cleaned_data['boiteVitesse']
        ancien_Annonce.puissanceFiscale = form_data.cleaned_data['puissanceFiscale']
        ancien_Annonce.energie = form_data.cleaned_data['energie']
        ancien_Annonce.kilometrage = form_data.cleaned_data['kilometrage']
        ancien_Annonce.prix = form_data.cleaned_data['prix']
        ancien_Annonce.save()
        msg='Annonce a été modifié avec succès'
    context={
        'form':form_data,
        'msg':msg
    }

    return render(request,'modifierAnnonce.html',context)

def afficherAnnonce(request, id):
    afficher_Annonce = Annonce.objects.filter(pk=id)[0]
    context={
        'Annonce':afficher_Annonce    
    }
    return render(request,'afficherAnnonce.html',context)

def Estimation(request):
    with open("marque.csv") as f:
        reader = csv.reader(f)
        next(reader)
        data = []
        for row in reader:
            data.append(row)
            
    with open("modele.csv") as f:
        reader = csv.reader(f)
        next(reader)
        modeles = []
        for row in reader:
            modeles.append(row)
    
    form_data = FormPrix(request.POST or None)
    msg = ''
    model_clone = joblib.load('my_model.pkl')
    if form_data.is_valid():
        vehicule_data = [[
            int(request.POST['marque']),
            int(request.POST['modele']),
            form_data.cleaned_data['kilometrage'],
            form_data.cleaned_data['annee'],
            form_data.cleaned_data['energie'],
            form_data.cleaned_data['boite'],
            form_data.cleaned_data['puissance']
        ]]
        prix = model_clone.predict(vehicule_data)
        msg = "resultat : " + str(int(prix[0])) + "DT"
    context = {
        'form': form_data,
        'marques': data,
        'modeles': modeles,
        'msg': msg
    }
    return render(request, 'calcul.html', context)

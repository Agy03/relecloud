from django.shortcuts import render, redirect
from django.db.models import Avg, FloatField
from django.db.models.functions import Coalesce
from django.urls import reverse_lazy
from . import models
from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .forms import ReviewForm
import random

def about(request):
    # Obtener todos los cruceros y seleccionar 3 aleatorios
    all_cruises = models.Cruise.objects.all()
    random_cruises = random.sample(list(all_cruises), min(len(all_cruises), 3))

    # Pasar los cruceros aleatorios a la plantilla
    return render(request, 'about.html', {
        'cruises': random_cruises
    })

# Vistas básicas
def index(request):
    destinations = models.Destination.objects.all()[:2]  # Trae los primeros 2 destinos
    return render(request, 'index.html', {'destinations': destinations})

def destinations(request):
    all_destinations = models.Destination.objects.all()  # Trae todos los destinos
    top_3_destinations = models.Destination.objects.annotate(
       average_rating=Coalesce(Avg('reviews__rating'), 0, output_field=FloatField())
       ).order_by('-average_rating')[:3]

    return render(request, 'destinations.html',  {
        'destinations': all_destinations,
        'top_3_destinations': top_3_destinations
    })


def cruises(request):
    all_cruises = models.Cruise.objects.all()  # Trae todos los cruceros
    return render(request, 'cruises.html', {'cruises': all_cruises})

# Vista para mostrar las reseñas y permitir agregar reseñas
def reviews(request):
    all_destinations = models.Destination.objects.all()  # Obtener todos los destinos
    all_cruises = models.Cruise.objects.all()  # Obtener todos los cruceros

    # Crear un formulario de reseña vacío
    review_form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            # Verificar si el formulario tiene un destino o un crucero
            if 'destination' in request.POST:
                review.destination = models.Destination.objects.get(id=request.POST['destination'])
            if 'cruise' in request.POST:
                review.cruise = models.Cruise.objects.get(id=request.POST['cruise'])
            review.save()
            messages.success(request, 'Reseña enviada correctamente!')
            return redirect('reviews')  # Redirigir a la página de reseñas

    return render(request, 'reviews.html', {
        'destinations': all_destinations,
        'cruises': all_cruises,
        'review_form': review_form,
    })

# Vista detalle para Destination
class DestinationDetailView(generic.DetailView):
    template_name = 'destination_detail.html'
    model = models.Destination
    context_object_name = 'destination'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        destination = self.object
        # Obtener reseñas de este destino
        context['reviews'] = destination.reviews.all()
        # Incluir el formulario para crear una reseña
        context['review_form'] = ReviewForm(initial={'destination': destination})
        return context

    def post(self, request, *args, **kwargs):
        destination = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.destination = destination
            review.save()
            return redirect('destination_detail', pk=destination.pk)
        else:
            context = self.get_context_data(**kwargs)
            context['review_form'] = form
            return self.render_to_response(context)

# Vista detalle para Cruise
class CruiseDetailView(generic.DetailView):
    template_name = 'cruise_detail.html'
    model = models.Cruise
    context_object_name = 'cruise'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cruise = self.object
        # Obtener reseñas de este crucero
        context['reviews'] = cruise.reviews.all()
        # Incluir el formulario para crear una reseña
        context['review_form'] = ReviewForm(initial={'cruise': cruise})
        return context

    def post(self, request, *args, **kwargs):
        cruise = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.cruise = cruise
            review.save()
            return redirect('cruise_detail', pk=cruise.pk)
        else:
            context = self.get_context_data(**kwargs)
            context['review_form'] = form
            return self.render_to_response(context)

# Crear InfoRequest con un formulario crispy
class InfoRequestCreate(SuccessMessageMixin, generic.CreateView):
    template_name = 'info_request_create.html'
    model = models.InfoRequest
    form_class = models.InfoRequestForm 
    success_url = reverse_lazy('index')
    success_message = 'Thank you, %(name)s! We will email you when we have more information about %(cruise)s!'

# CRUD para Destination
class DestinationCreateView(generic.CreateView):
    model = models.Destination
    form_class = models.DestinationForm
    template_name = 'destination_form.html'
    success_url = reverse_lazy('destinations')
    enctype = "multipart/form-data"  # Asegurar que se acepten archivos en la carga

class DestinationUpdateView(generic.UpdateView):
    model = models.Destination
    form_class = models.DestinationForm
    template_name = 'destination_form.html'
    success_url = reverse_lazy('destinations')

class DestinationDeleteView(generic.DeleteView):
    model = models.Destination
    template_name = 'destination_confirm_delete.html'
    success_url = reverse_lazy('destinations')

# CRUD para Cruise
class CruiseCreateView(generic.CreateView):
    model = models.Cruise
    form_class = models.CruiseForm
    template_name = 'cruise_form.html'
    success_url = reverse_lazy('index')
    enctype = "multipart/form-data"  # Asegurar que se acepten archivos en la carga

class CruiseUpdateView(generic.UpdateView):
    model = models.Cruise
    form_class = models.CruiseForm
    template_name = 'cruise_form.html'
    success_url = reverse_lazy('index')

class CruiseDeleteView(generic.DeleteView):
    model = models.Cruise
    template_name = 'cruise_confirm_delete.html'
    success_url = reverse_lazy('index')



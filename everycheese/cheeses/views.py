
import logging
log = logging.getLogger("root")
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from .models import Cheese
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from django.http import request
from .models import Cheese, Rating  # Import the Rating model

class CheeseListView(ListView):
    model = Cheese
class CheeseDetailView(DetailView):
    model = Cheese
class CheeseCreateView(LoginRequiredMixin, CreateView):

    model = Cheese
    fields = [
        'name',
        'description',
        'firmness',
        'country_of_origin',
    ]
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
class CheeseUpdateView(LoginRequiredMixin, UpdateView):
    model = Cheese
    fields = [
        'name',
        'description',
        'firmness',
        'country_of_origin',
    ]
    action = "Update"


    def get_context_data(self, **kwargs):
        log.info("Hello from update")
        ctx = super(CheeseUpdateView, self).get_context_data(**kwargs)
        _slug = self.kwargs.get("slug")
        ch = Cheese.objects.all().filter(slug=_slug).first()

        if ch is None:
            ctx["rating"] = 0
            return ctx

        r = Rating.objects.all().filter(creator=self.request.user, cheese=ch).first()

        if r is not None:
            ctx["rating"] = r.i_rating
        else:
            ctx["rating"] = 0

        return ctx

    def form_valid(self, form):
        # Get the cheese being updated
        cheese = self.object

        # Get or create the rating for the current user and cheese
        rating, created = Rating.objects.get_or_create(creator=self.request.user, cheese=cheese)

        # Update the rating value based on the form data
        rating.i_rating = int(self.request.POST.get('rating'))  # Safely retrieve the rating value
        rating.save()

        return super().form_valid(form)

     


class CheeseDeleteView(LoginRequiredMixin, DeleteView):
    model = Cheese
    success_url = reverse_lazy('cheeses:list')  # Redirect to the list view after deletion

# Add the delete_cheese view function here
def delete_cheese(request, slug):
    cheese = Cheese.objects.get(slug=slug)
    
    if request.method == 'POST':
        # Delete the cheese if the request method is POST
        cheese.delete()
        return redirect('cheeses:list')  # Redirect to the list view after deletion
    
    return render(request, 'cheese_confirm_delete.html', {'cheese': cheese})
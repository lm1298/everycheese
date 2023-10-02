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
        'country_of_origin'
    ]
    action = "Update"
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
from django.urls import path
from . import views
app_name = "cheeses"
urlpatterns = [
    path(
        route='',
        view=views.CheeseListView.as_view(),
        name='list'
    ),
    path(
        route='add/',
        view=views.CheeseCreateView.as_view(),
        name='add'
    ),
    path(
        route='<slug:slug>/update/',
        view=views.CheeseUpdateView.as_view(),
        name='update'
    ),

    path(
        route='<slug:slug>/',
        view=views.CheeseDetailView.as_view(),
        name='detail'
    ),
    path('<slug:slug>/delete/', views.CheeseDeleteView.as_view(), name='confirm_delete'),

    # URL pattern for the delete view function (no change needed here)
    path('<slug:slug>/delete/confirm/', views.delete_cheese, name='delete_cheese'),

]

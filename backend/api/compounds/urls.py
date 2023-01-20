from django.urls import path

from api.compounds import views

urlpatterns = [path("", views.Compounds.as_view())]

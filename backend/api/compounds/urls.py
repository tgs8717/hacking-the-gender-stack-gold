from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import Compounds

router = DefaultRouter()
router.register("", Compounds, "compounds")

urlpatterns = [path("", include(router.urls))]

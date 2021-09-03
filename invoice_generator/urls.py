from django.urls import path
from invoice_generator.views import HomeView, SearchView

urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path("search/", SearchView.as_view(), name='search'),
]

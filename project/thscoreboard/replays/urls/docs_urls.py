from django.urls import path

from replays.views import docs


urlpatterns = [
    path('', docs.make_docs_page_route('about.html')),
]

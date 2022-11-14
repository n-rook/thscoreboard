from django.urls import path

from replays.views import docs


urlpatterns = [
    path('', docs.make_docs_page_route('about.html'), name='Docs/About'),
    path('terms', docs.make_docs_page_route('terms_of_use.html'), name='Docs/TermsOfUse'),
    path('privacy', docs.make_docs_page_route('privacy_policy.html'), name='Docs/Privacy'),
    path('rules', docs.make_docs_page_route('rules.html'), name='Docs/Rules'),
    path('replayrules', docs.make_docs_page_route('replay_rules.html'), name='Docs/Replay Rules'),
]

"""Contains functions to show mostly-static documentation pages."""

from django.shortcuts import render
from django.views.decorators import http as http_decorators


def make_docs_page_route(template_name: str):
    """Create a simple route to render a docs page."""

    @http_decorators.require_safe
    def route(request):
        return render(request, f"replays/docs/{template_name}")

    return route

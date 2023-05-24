from django.shortcuts import render
from django.contrib.auth import decorators as auth_decorators
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse

import users.models as user_models


@auth_decorators.login_required
def my_claims(request: WSGIRequest) -> HttpResponse:
    claim_requests = user_models.ClaimReplayRequest.objects.order_by("id")
    if not request.user.is_staff:
        claim_requests = claim_requests.filter(user=request.user).all()
    return render(
        request,
        "replays/my_claims.html",
        {"claim_requests": claim_requests},
    )

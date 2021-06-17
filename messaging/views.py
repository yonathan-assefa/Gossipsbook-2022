from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def conntect_websocket(request, username):
    print(request.user)
    user_obj = get_object_or_404(User, username=username)
    context = {
        "user_chating_with": user_obj,
    }
    return render(request, "chating.html", context)

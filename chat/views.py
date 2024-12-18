from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
# Create your views here.


def index(request):

    return render(request, "chat/index.html")

def room(request, room_name):
    user_name = request.user.username
    context = {
        "room_name": room_name,
         "user_name": mark_safe(json.dumps(user_name)),
    }
    return render(request, "chat/room.html", context)

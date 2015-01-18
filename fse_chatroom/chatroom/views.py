from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from chatroom.models import *

def index(request):
    chatlist = ChatRoom.objects.order_by('name')
    context = {}

    context['chatlist'] = chatlist

    return render(request, 'chatroom/index.html', context)

def chatroom(request, chatroom_id):
    chat = get_object_or_404(ChatRoom, id=chatroom_id)
    context = {}

    context['chat'] = chat

    return render(request, 'chatroom/chatroom.html', context)

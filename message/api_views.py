import urllib
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User, AnonymousUser
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from message.serializers import *
from message.models import Badword
from user.models import Profile


@csrf_exempt
def create_message(request, chat_id):
    if request.method != "POST":
        return JsonResponse({}, status=400)
    body = urllib.parse.parse_qs(request.body.decode())
    [message] = body.get('message')
    if not message:
        return JsonResponse({'message': 'Field "message" is required.'}, status=400)

    message = censor_badwords(message)
    chat = chat_id
    try:
        Chat.objects.get(id=chat)
    except Chat.DoesNotExist:
        return JsonResponse({'Chat does not exist.'}, status=400)

    msg = Message(text=message, user=Profile.objects.get(user=request.user), chat_id=chat)
    msg.save()
    return redirect(reverse("render_chat", kwargs={'chat_id': chat_id}))


def replace_symbols(source, target, replacer):
    result = ""
    previous_index = 0
    source_lower = source.lower()
    target_lower = target.lower()

    index = source_lower.find(target_lower)

    while index != -1:
        result += source[previous_index:index]
        result += replacer * len(target)

        previous_index = index + len(target)
        index = source_lower.find(target_lower, previous_index)

    result += source[previous_index:len(source)]
    return result


def censor_badwords(message):
    badwords = Badword.objects.all()

    for badword in badwords:
        message = replace_symbols(message, badword.word, "*")

    return message


@csrf_exempt
def delete_message(request, message_id):
    if request.method != "POST":
        return JsonResponse({}, status=400)
    try:
        message = Message.objects.get(id=message_id)
        chat_id = message.chat.id
        message.delete()
        return redirect(reverse("render_chat", kwargs={'chat_id': chat_id}))
    except Message.DoesNotExist:
        return JsonResponse({'Message does not exist'}, status=400)


@csrf_exempt
def create_chat(request):
    if request.method == "POST":
        body = urllib.parse.parse_qs(request.body.decode())
        [name] = body.get('name')
        chat = Chat(name=name)
        chat.save()
    return redirect(reverse("render_list"))

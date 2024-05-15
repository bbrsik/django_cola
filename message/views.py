from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from message.serializers import serialize_chats, serialize_messages
from message.models import Chat, Message
from user.models import Profile
from weather.models import Weather
from weather.utility import should_update_weather, request_weather_data


def render_chat(request, chat_id):
    if not request.user.is_authenticated:
        return redirect('/user/login/')
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        return JsonResponse({'Response': 'Chat does not exist'}, status=404)
    message_set = serialize_messages(Message.objects.filter(chat_id=chat_id))
    chat_has_messages = bool(len(message_set))
    context = {
        'chat_id': chat_id,
        'name': chat.name,
        'messages': message_set,
        'chat_has_messages': chat_has_messages,
    }
    return render(request, 'render_chat.html', context=context)


def render_list(request):
    if not request.user.is_authenticated:
        return redirect('/user/login/')
    chats = serialize_chats(Chat.objects.all())
    profile = Profile.objects.get(user=request.user)
    if should_update_weather(profile.current_location):
        try:
            weather_data = request_weather_data(profile.current_location)
            weather_to_save = Weather(**weather_data)
            weather_to_save.save()
        except Exception as e:
            print('Error while requesting weather', e)
    try:
        weather = Weather.objects.filter(location=profile.current_location).latest('created_at')
    except ObjectDoesNotExist:
        weather = None

    context = {
        'chats': chats,
        'weather': weather,
    }
    return render(request, 'render_list.html', context=context)

from django.http import JsonResponse
from django.shortcuts import render, redirect
from message.serializers import serialize_chats, serialize_messages
from message.models import Chat, Message
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

    if should_update_weather():
        try:
            weather_data = request_weather_data()
            weather_to_save = Weather(**weather_data)
            weather_to_save.save()
        except Exception as e:
            print('Error while requesting weather', e)

    weather = Weather.objects.all().order_by('created_at').last()
    context = {
        'chats': chats,
        'weather': weather,
    }
    return render(request, 'render_list.html', context=context)

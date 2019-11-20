from django.contrib.auth import authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.template import loader
from rest_framework.response import Response

import psycopg2


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'code': HTTP_200_OK * 100,
        'data': {
            'token': token.key
        }
    }, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def MyToken(request):
    tok = request.data.get("token")
    print(tok)
    context = {'token': tok}

    conn = psycopg2.connect(dbname='military', user='marat', password='marat', host='0.0.0.0')
    cursor = conn.cursor()
    cursor.execute('SELECT * ')

    return render(request, 'info/token.html', context)
    #messages.info(request, request.to_string())
    #return render_to_response('template_name', message='Save complete')
    #data = {'sample_data': 123}
    #return Response(data, status=HTTP_200_OK)

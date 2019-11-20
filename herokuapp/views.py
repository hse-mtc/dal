from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response


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
def info(request):
    data = {
        'roles': ['admin'],
        'introduction': 'I am a administrator',
        'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        'name': 'Пеляк В.С.'
    }

    if request.user.username != 'sampleuser':
        data['roles'] = ['editor']
        data['name'] = 'editor'

    return Response({
        'code': HTTP_200_OK * 100,
        'data': data
    }, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def logout(request):
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass

    return Response({
        'code': HTTP_200_OK * 100,
        'data': 'success'
    }, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def documents(request):
    data = {
        'total': 3,
        'items': [
            {
                'id': 1,
                'title': 'Особенности организации и проведения военно-научной работы на военной кафедре',
                'authors': ['Коргутов В.А.',
                            'Пеляк В.С.'],
                'annotation': 'В статье проанализированы требования руководящих нормативных документов, регламентирующих '
                              'организацию военно-научной работы на военных кафедрах при государственных образовательных '
                              'организациях высшего образования, и предложены инновационные подходы по вопросам '
                              'интеграции военной науки и военного образования в интересах повышения качества подготовки '
                              'студентов по действующим учебным программам.',
                'keywords': [],
                'status': 'enabled',  # (enabled, created, hidden)
                'publish_at': "2014-09-08T08:02:17-05:00",
                'publish_places': 'Журнал 1'
            },
            {
                'id': 2,
                'title': 'Расширение возможностей экологического мониторинга с помощью рамановской спектроскопии',
                'authors': ['Пеляк В.С.', 'Кузин А.Ю.'],
                'annotation': 'Одной из самых актуальных тем в наше время является экологический мониторинг окружающей '
                              'среды. В данной работе предлагается концепция использования рамановской спектроскопии для '
                              'своевременного контроля состояния и обстановки природной среды.',
                'keywords': [],
                'status': 'enabled',  # (enabled, created, hidden)
                'publish_at': "2015-09-08T08:02:17-05:00",
                'publish_places': 'Журнал 2'
            },
            {
                'id': 3,
                'title': 'Подход к определению рационального содержания военной подготовки офицеров запаса в военных '
                         'учебных центрах при гражданских образовательных организациях',
                'authors': ['Семенов П.Ю.',
                            'Пеляк В.С.',
                            'Репалов Д.Н.',
                            'Никандров И.В.'],
                'annotation': '',
                'keywords': [],
                'status': 'enabled',  # (enabled, created, hidden)
                'publish_at': "2016-09-08T08:02:17-05:00",
                'publish_places': 'Журнал 3'
            }
        ]}
    return Response({
        'code': HTTP_200_OK * 100,
        'data': data
    }, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def nir(request):
    data = {
        'total': 1,
        'items': [
            {
                'id': 1,
                'title': 'Особенности организации и проведения военно-научной работы на военной кафедре',
                'authors': ['Коргутов В.А.',
                            'Пеляк В.С.'],
                'annotation': 'В статье проанализированы требования руководящих нормативных документов, регламентирующих '
                              'организацию военно-научной работы на военных кафедрах при государственных образовательных '
                              'организациях высшего образования, и предложены инновационные подходы по вопросам '
                              'интеграции военной науки и военного образования в интересах повышения качества подготовки '
                              'студентов по действующим учебным программам.',
                'keywords': [],
                'status': 'enabled',  # (enabled, created, hidden)
                'publish_at': "2014-09-08T08:02:17-05:00",
                'publish_places': 'Журнал 1'
            }
        ]}
    return Response({
        'code': HTTP_200_OK * 100,
        'data': data
    }, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def subjects(request):
    data = [
        {
            'id': 1,
            'title': 'ТП'
        },
        {
            'id': 2,
            'title': 'ВСП'
        },
        {
            'id': 3,
            'title': 'ТП(РХБЗ)'
        },
        {
            'id': 4,
            'title': 'ТП(В-ИП)'
        },
        {
            'id': 5,
            'title': 'ОП'
        },
        {
            'id': 6,
            'title': 'Матеша'
        },
        {
            'id': 7,
            'title': 'Русский',
        },
        {
            'id': 8,
            'title': 'АКОС'
        }
    ]
    return Response({
        'code': HTTP_200_OK * 100,
        'data': data
    }, status=HTTP_200_OK)

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

from herokuapp.models import Subjects, Documents, PublishPlaces, UserProfileInfo


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
        'avatar': request.user.userprofileinfo.profile_pic,
        'name': request.user.userprofileinfo.name,
    }

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
    authors = request.query_params.get('authors')
    start_time = request.query_params.get('start_time')
    end_time = request.query_params.get('end_time')
    publish_places = request.query_params.get('publish_places')

    db_request = Documents.objects.filter()
    if authors is not None:
        db_request = db_request.filter(authors__name__in=authors.split(','))
    if start_time is not None:
        db_request = db_request.filter(published_at__gte=start_time)
    if end_time is not None:
        db_request = db_request.filter(published_at__lte=end_time)
    if publish_places is not None:
        db_request = db_request.filter(published_places__place__in=publish_places.split(','))

    db_request.order_by('-published_at')

    data = {
        'items': list(
            map(lambda item: {
                'id': item.id,
                'title': item.title,
                'authors': list(item.authors.values_list('name', flat=True)),
                'annotation': item.annotation,
                'keywords': list(item.keywords.names()),
                'status': item.status.status,
                'publish_at': item.published_at.isoformat(),
                'publish_places': item.published_places.place
            },
                list(db_request)
                )
        )
    }
    data['total'] = len(data['items'])

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
    data = list(map(lambda x: {'id': x.id, 'title': x.title}, list(Subjects.objects.all())))
    return Response({
        'code': HTTP_200_OK * 100,
        'data': data
    }, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def educational_materials(request):  # TODO: Добавить параметр айди предмета
    data = [
        {
            'id': 1,
            'title': 'Матеша',
            'subject': {
                'id': 1,
                'title': 'Subject'
            },
            'lectures': [
                {
                    'id': 1,
                    'title': 'Справочник по матеше',
                    'url': '',
                    'edited': '2014-09-08T08:02:17-05:00',
                    'created': '2014-09-08T08:02:17-05:00'
                },
                {
                    'id': 2,
                    'title': 'Справочник по матеше 2',
                    'url': '',
                    'edited': '2014-09-08T08:02:17-05:00',
                    'created': '2014-09-08T08:02:17-05:00'
                }
            ],
            'seminars': [
                {
                    'id': 1,
                    'title': 'Семинар по матеше',
                    'url': '',
                    'edited': '2014-09-08T08:02:17-05:00',
                    'created': '2014-09-08T08:02:17-05:00'
                },
                {
                    'id': 2,
                    'title': 'Семинар по матеше 2',
                    'url': '',
                    'edited': '2014-09-08T08:02:17-05:00',
                    'created': '2014-09-08T08:02:17-05:00'
                }
            ]
        }
    ]
    return Response({
        'code': HTTP_200_OK * 100,
        'data': data
    }, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def authors(request):
    return Response({
        'code': HTTP_200_OK * 100,
        'data': list(
            map(lambda x:
                {
                    'label': x,
                    'value': x
                },
                UserProfileInfo.objects.values_list('name', flat=True)
                )
        )
    }, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def published_places(request):
    return Response({
        'code': HTTP_200_OK * 100,
        'data': list(
            map(lambda x:
                {
                    'label': x,
                    'value': x,
                },
                PublishPlaces.objects.values_list('place', flat=True)
                )
        )
    }, status=HTTP_200_OK)

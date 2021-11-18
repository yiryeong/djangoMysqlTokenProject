import jwt
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from payhistory.models import User, PayHistory
from payhistory.serializer import UserSerializer, HistorySerializer
from django.contrib.auth.hashers import check_password
from django_mysql_project.settings import SIMPLE_JWT


def token_decode(request):
    access_token = request.META['HTTP_AUTHORIZATION']
    payload = jwt.decode(
        access_token.split(' ')[1],
        SIMPLE_JWT['SIGNING_KEY'],
        algorithms=[SIMPLE_JWT['ALGORITHM']],
    )
    return payload


# 권한 있어야 접근가능
@permission_classes([IsAuthenticated])
class GetUserList(APIView):
    def get(self, request):
        query_set = User.objects.all()
        serializer = UserSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)


# 누구나 접근가능
@permission_classes([AllowAny])
class RegistUser(APIView):
    def post(self, request):
        serializer = UserSerializer(request.data)
        email = serializer.data['email']

        if User.objects.filter(email=email).exists():
            # DB에 있는 값 user 객체에 담음
            user = User.objects.filter(email=email)
            data = dict(
                msg="이미 존재하는 메일입니다.",
                email=user.first().email
            )
            return Response(data)

        user = serializer.create(request.data)
        return Response(dict(data=UserSerializer(user).data, msg="회원가입 성공", status=201))


# 누구나 접근가능
@permission_classes([AllowAny])
class Login(APIView):
    def post(self, request):
        email = request.data.get('email', "")
        password = request.data.get('password', "")
        user = User.objects.filter(email=email).first()

        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        token = {
            'access': access_token,
            'refresh': refresh_token,
        }

        if user is None:
            return Response(dict(msg="로그인 메일이 존재하지 않습니다.", email=email, status=400))

        if check_password(password, user.password):
            return Response(dict(msg="로그인 성공", uid=user.uid, token=token, status=200))
        else:
            return Response(dict(msg="로그인 실패", status=400))


# 권한 있어야 접근가능
@permission_classes([IsAuthenticated])
class HistoryList(APIView):
    def get(self, request):
        payload = token_decode(request)
        query_set = PayHistory.objects.filter(uid=payload['uid'])
        serializer = HistorySerializer(query_set, many=True)
        return JsonResponse(serializer.data, json_dumps_params={'ensure_ascii': False}, safe=False, status=200)


# 권한 있어야 접근가능
@permission_classes([IsAuthenticated])
class CreateHistory(APIView):
    def post(self, request):
        payload = token_decode(request)
        request_data = request.data
        request_data['uid'] = payload['uid']
        serializer = HistorySerializer(request_data)
        history = PayHistory.objects.filter(datetime=serializer.data['datetime'])
        if history:
            data = dict(
                msg="해당 데이터는 이미 존재합니다.",
                datetime=history.first().datetime,
                price=history.first().price
            )
            return Response(data)

        history = serializer.create(request_data)
        return Response(data=HistorySerializer(history).data, status=201)


# 권한 있어야 접근가능
@permission_classes([IsAuthenticated])
class UpdateHistory(APIView):
    def put(self, request, id):
        payload = token_decode(request)
        uid = payload['uid']
        request_data = request.data
        try:
            query_set = PayHistory.objects.get(id=id)
            if query_set.uid != uid:
                return Response("해당 데이터의 수정 권한이 없습니다.", status=status.HTTP_400_BAD_REQUEST)
            else:
                request_data['uid'] = payload['uid']
        except PayHistory.DoesNotExist:
            return HttpResponse(status=404)

        serializer = HistorySerializer(query_set, data=request_data)
        if serializer.is_valid():
            serializer.save()
            response = dict(
                msg="정상 수정 되었습니다.",
                data=serializer.data,
                status=200
            )
            return Response(response)
        return Response("잘못된 요청", status=status.HTTP_400_BAD_REQUEST)


# 권한 있어야 접근가능
@permission_classes([IsAuthenticated])
class DeleteHistory(APIView):
    def delete(self, request, id):
        payload = token_decode(request)
        uid = payload['uid']
        try:
            query_set = PayHistory.objects.get(id=id)
            if query_set.uid != uid:
                return Response("해당 데이터의 삭제 권한이 없습니다.", status=status.HTTP_400_BAD_REQUEST)
        except PayHistory.DoesNotExist:
            return HttpResponse(status=404)

        query_set.delete()
        response = dict(
            msg="정상 삭제 되었습니다.",
            status=200
        )
        return Response(response)

from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from payhistory.models import User, PayHistory
from payhistory.serializer import UserSerializer, HistorySerializer
from django.contrib.auth.hashers import check_password


class GetUserList(APIView):
    def get(self, request):
        query_set = User.objects.all()
        serializer = UserSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)


class Login(APIView):
    def post(self, request):
        email = request.data.get('email', "")
        password = request.data.get('password', "")
        user = User.objects.filter(email=email)

        if user is None:
            return Response(dict(msg="로그인 메일이 존재하지 않습니다."))
        if check_password(password, user.password):
            return Response(dict(msg="로그인 성공", email=user.email))
        else:
            return Response(dict(msg="로그인 실패"))


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
        return Response(data=UserSerializer(user).data)


class HistoryList(APIView):
    def get(self, request):
        query_set = PayHistory.objects.all()
        serializer = HistorySerializer(query_set, many=True)
        return JsonResponse(serializer.data, json_dumps_params={'ensure_ascii': False}, safe=False, status=200)


class CreateHistory(APIView):
    def post(self, request):
        serializer = HistorySerializer(request.data)
        history = PayHistory.objects.filter(datetime=serializer.data['datetime'])
        if history:
            data = dict(
                msg="해당 데이터는 이미 존재합니다.",
                datetime=history.first().datetime,
                price=history.first().price
            )
            return Response(data)

        history = serializer.create(request.data)
        return Response(data=HistorySerializer(history).data, status=200)


class UpdateHistory(APIView):
    def put(self, request, id):
        try:
            query_set = PayHistory.objects.get(id=id)
        except PayHistory.DoesNotExist:
            return HttpResponse(status=404)

        serializer = HistorySerializer(query_set, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("정상 수정 되었습니다.", status=200)
        return Response("잘못된 요청", status=status.HTTP_400_BAD_REQUEST)


class DeleteHistory(APIView):
    def delete(self, request, id):
        try:
            query_set = PayHistory.objects.get(id=id)
        except PayHistory.DoesNotExist:
            return HttpResponse(status=404)

        query_set.delete()
        return Response("정상 삭제 되었습니다.", status=200)

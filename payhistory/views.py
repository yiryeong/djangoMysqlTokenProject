import jwt
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from payhistory.models import User, PayHistory
from payhistory.serializer import UserSerializer, HistorySerializer
from django.contrib.auth.hashers import check_password
from django_mysql_project.settings import SIMPLE_JWT


def decode_token(request):
    """
       token decode function
    """
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

        """
            로그인 된 상태에서 사용자 정보 조회 함수
            request에 유효한 token으로 요청 시 정상 조회 가능
        """

        query_set = User.objects.all()
        serializer = UserSerializer(query_set, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


# 누구나 접근가능
@permission_classes([AllowAny])
class RegisterUser(APIView):

    serializer_class = UserSerializer

    def post(self, request):

        """
            request.data에 포함된 내용
                @email : 회원가입할 이메일
                @password : 회원가입할 비밀번호

            비밀번호를 단방향 암호화 후 회원가입(계정 생성)
        """

        serializer = self.serializer_class(request.data)
        email = serializer.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.filter(email=email)
            data = dict(
                msg="이미 존재하는 메일입니다.",
                email=user.first().email
            )
            return Response(data, status=status.HTTP_409_CONFLICT)

        user = serializer.create(request.data)
        return Response(dict(data=self.serializer_class(user).data, msg="회원가입 성공"), status=status.HTTP_201_CREATED)


# 누구나 접근가능
@permission_classes([AllowAny])
class Login(APIView):

    def post(self, request):

        """
            request에 포함된 내용
                @email : 로그인할 이메일
                @password : 비밀번호

            요청 메일이 존재하지 않을 경우 "로그인 메일이 존재하지 않습니다." 메세지 반환
            로그인 메일이 존재하며 비밀번호가 디비에 비번과 같을 경우 정상 로그인 되며 token 생성하여 반환
        """

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
            return Response(dict(msg="로그인 메일이 존재하지 않습니다.", email=email), status=status.HTTP_400_BAD_REQUEST)

        if check_password(password, user.password):
            return Response(dict(msg="로그인 성공", uid=user.uid, token=token), status=status.HTTP_200_OK)
        else:
            return Response("로그인 실패", status=status.HTTP_400_BAD_REQUEST)


# 권한 있어야 접근가능
@permission_classes([IsAuthenticated])
class HistoryList(APIView):

    serializer_class = HistorySerializer

    def get(self, request):

        """
            로그인 된 상태에서 해당 계정의 가계부 내역 조회 함수
            request에 유효한 token으로 요청 시 정상 조회 가능
        """

        payload = decode_token(request)
        query_set = PayHistory.objects.filter(uid=payload['uid'])
        serializer = self.serializer_class(query_set, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


# 권한 있어야 접근가능
@permission_classes([IsAuthenticated])
class CreateHistory(APIView):
    def post(self, request):

        """
            로그인 된 상태(유효한 token으로 요청 시)에서 해당 계정의 가계부 내역 추가 함수

            request에 포함된 내용
                @datetime : 데이터 추가하는 현제 시간
                @price : 가격
                @memo : 메모

            디비에 이미 해당 시간의 데이터가 존재 할 경우 "해당 데이터는 이미 존재합니다." 메세지 리턴
                                    없을 경우 해당 데이터 추가

        """

        payload = decode_token(request)
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
            return Response(data, status=status.HTTP_409_CONFLICT)

        history = serializer.create(request_data)
        return Response(data=HistorySerializer(history).data, status=status.HTTP_201_CREATED)


# 권한 있어야 접근가능
@permission_classes([IsAuthenticated])
class UpdateHistory(APIView):
    def put(self, request, id):

        """
            로그인 된 상태(유효한 token으로 요청 시)에서 해당 계정의 가계부 내역 수정 함수

            @id 가계부 내역의 리코드 아이디

            request에 포함된 내용
                @datetime : 데이터 수정하는 현제 시간
                @price : 가격
                @memo : 메모

            요청 데이터의 uid가 로그인 uid와 다른 경우 "해당 데이터의 수정 권한이 없습니다." 메세지 리턴
            수정할 데이터가 존재 하지 않을 경우 403 리턴
            요청 데이터가 유효 할 경우 정상 수정 가능 "정상 수정 되었습니다." 메세지 리턴
        """

        payload = decode_token(request)
        uid = payload['uid']
        request_data = request.data

        try:
            query_set = PayHistory.objects.get(id=id)
            if query_set.uid != uid:
                return Response("해당 데이터의 수정 권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)
            else:
                request_data['uid'] = payload['uid']
        except PayHistory.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        serializer = HistorySerializer(query_set, data=request_data)
        if serializer.is_valid():
            serializer.save()
            response = dict(
                msg="정상 수정 되었습니다.",
                data=serializer.data
            )
            return Response(response, status=status.HTTP_201_CREATED)
        return Response("잘못된 요청", status=status.HTTP_400_BAD_REQUEST)


# 권한 있어야 접근가능
@permission_classes([IsAuthenticated])
class DeleteHistory(APIView):
    def delete(self, request, id):

        """
            로그인 된 상태(유효한 token으로 요청 시)에서 해당 계정의 가계부 내역 삭제 함수

            @id 가계부 내역의 리코드 아이디

            요청 데이터의 uid가 로그인 uid와 다른 경우 "해당 데이터의 삭제 권한이 없습니다." 메세지 리턴
            수정할 데이터가 존재 하지 않을 경우 403 리턴
            요청 데이터가 유효 할 경우 정상 삭제 가능 "정상 삭제 되었습니다." 메세지 리턴
        """

        payload = decode_token(request)
        uid = payload['uid']

        try:
            query_set = PayHistory.objects.get(id=id)
            if query_set.uid != uid:
                return Response("해당 데이터의 삭제 권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)
        except PayHistory.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        query_set.delete()
        return Response("정상 삭제 되었습니다.", status=status.HTTP_200_OK)


# 권한 있어야 접근가능
@permission_classes([IsAuthenticated])
class Logout(APIView):
    def post(self, request):

        """
             로그인 된 상태(유효한 token으로 요청 시)에서 로그아웃 함수

             로그인중 정상 생성된 refresh token으로 로그아웃 요청
        """

        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response("로그아웃 되었습니다.", status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

import jwt
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from user.models import User
from user.serializer import UserSerializer
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

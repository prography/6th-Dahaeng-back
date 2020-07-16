from django.shortcuts import redirect
from rest_framework import permissions, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from core.social_login.kakao_social_login import KakaoSocialLogin
from core.models import Profile
from .serializers import ProfileSerializer
import json
from uuid import uuid4
import requests
# from accounts.social_login.naver_social_login import NaverSocialLogin


class UserSocialViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]
    state_token_code = uuid4().hex

    def __init__(self, **kwargs):
        self.kakao_social_login = KakaoSocialLogin()
        # self.naver_social_login = NaverSocialLogin(self.state_token_code
        super(UserSocialViewSet, self).__init__(**kwargs)

    @action(detail=False, methods=['get'], url_path='kakao_login')
    def get_kakao_auth_token(self, request, pk=None):
        url = self.kakao_social_login.get_auth_url()
        return redirect(url)

    @action(detail=False, methods=['get'], url_path='kakao_login_callback')
    def kakao_login_callback(self, request, pk=None):
        try:
            user_data_per_field = self.kakao_social_login.get_user_data(
                request)
        except Exception as e:
            return self.error_with_message(e)

        if self._have_already_sign_up_for_other_social(user_data_per_field):
            what_social_did_user_already_sign_up = Profile.objects.get(
                email=user_data_per_field['email']).social
            return Response({
                'message': f'이미 {what_social_did_user_already_sign_up}로 가입했습니다. {what_social_did_user_already_sign_up}로 로그인 해주세요.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if Profile.objects.filter(email=user_data_per_field['email'], social=user_data_per_field['social']):
            user = self.kakao_social_login.login(user_data_per_field)
        else:
            user = self.kakao_social_login.sign_up(user_data_per_field)

        URL = 'http://'+request.META['HTTP_HOST'] + '/login/'
        data = {
            'email': user.email,
            'password': user.password
        }
        response = requests.post(URL, data=data)
        breakpoint()
        # refresh = CustomUserObtainPairSerializer.get_token(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

    def error_with_message(self, e):
        if e.args:
            detail = e.args[0]
            error_name = e.__class__.__name__
        return Response({"message": f'{error_name}가 발생했습니다. {detail}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _have_already_sign_up_for_other_social(self, user_data_per_field):
        user = Profile.objects.filter(email=user_data_per_field['email'])
        if user.count() > 1:
            raise AssertionError('해당 이메일로 가입된 계정이 이미 존재합니다. 관리자에게 문의해주세요.')
        if user.count() == 1:
            user = user[0]
            return user.social != user_data_per_field['social']
        return False

    # @action(detail=False, methods=['get'], url_path='naver-login')
    # def get_naver_auth_token(self, request, pk=None):
    #     url = self.naver_social_login.get_auth_url()
    #     return redirect(url)

    # @action(detail=False, methods=['get'], url_path='naver-login-callback')
    # def naver_login_callback(self, request, pk=None):
    #     callback_status_token_code = request.query_params.get('state')
    #     if callback_status_token_code != self.naver_social_login.state_token_code:
    #         return Response({'message': 'state token code is not valid'}, status=status.HTTP_401_UNAUTHORIZED)

    #     try:
    #         user_data_per_field = self.naver_social_login.get_user_data(
    #             request)
    #     except Exception as e:
    #         return self.error_with_message(e)

    #     if self._have_already_sign_up_for_other_social(user_data_per_field):
    #         what_social_did_user_already_sign_up = User.objects.get(
    #             email=user_data_per_field['email']).social
    #         return Response({
    #             'message': f'이미 {what_social_did_user_already_sign_up}로 가입했습니다. {what_social_did_user_already_sign_up}로 로그인 해주세요.'
    #         }, status=status.HTTP_400_BAD_REQUEST)

    #     if User.objects.filter(email=user_data_per_field['email'], social=user_data_per_field['social']):
    #         user = self.naver_social_login.login(user_data_per_field)
    #     else:
    #         user = self.naver_social_login.sign_up(user_data_per_field)

    #     refresh = CustomUserObtainPairSerializer.get_token(user)
    #     return Response({
    #         'refresh': str(refresh),
    #         'access': str(refresh.access_token)
    #     })

    # def _naver_login_or_sign_up(self, snowflake_user_data):
    #     email = snowflake_user_data['email']
    #     social = snowflake_user_data['social']
    #     user = User.objects.filter(email=email)

    #     if user.exists():
    #         user = User.objects.get(email=email)
    #         if user.social == social:
    #             user = naver.login(snowflake_user_data)
    #             return user
    #         else:
    #             already_signup_social = user.social
    #             if already_signup_social == 'NONE':
    #                 already_signup_social = "눈송이"
    #             return already_signup_social

    #     user = naver.sign_up(snowflake_user_data)
    #     return user


# https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code
# https://kauth.kakao.com/oauth/authorize?client_id=ea0c660893539d787993dada9b5ccba2&redirect_uri=http://localhost:8000/social/kakao_login_callback/&response_type=code

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer


class RegistrationView(APIView):

    """
    View for user registration.    

    Permissions:
        AllowAny: Anyone can register.

    POST:
        Receives: JSON with 'email', 'fullname', 'password'.
        email and fullname must be unique.
        Creates a new user and returns a success message or error details.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            data = {"detail": "User created successfully!"}
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):

    """
    View for user login.

    Permissions:
        AllowAny: Anyone can attempt to log in.

    POST:
        Receives: JSON with 'username' and 'password'.
        Returns: Sets 'access' and 'refresh' tokens in HttpOnly cookies and returns user details on successful authentication.
    """

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e

        acess = serializer.validated_data.get('access')
        refresh = serializer.validated_data.get('refresh')
        user = serializer.user

        response = Response(
            {
                "detail": "Login successfully!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key='access_token',
            value=acess,
            httponly=True,
            secure=True,
            samesite='Lax',
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh,
            httponly=True,
            secure=True,
            samesite='Lax',
        )

        return response


class RefreshTokenView(TokenRefreshView):

    """
    View for refreshing JWT access tokens.

    Permissions:
        AllowAny: Anyone can attempt to refresh the token.

        POST:
            Receives: No body required, uses 'refresh_token' from HttpOnly cookie.
            Returns: Sets a new 'access' token in an HttpOnly cookie and returns a success message.

    """

    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            return Response({"detail": "Refresh token not provided."},status=status.HTTP_400_BAD_REQUEST )
        serializer = self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
           return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)

        acess = serializer.validated_data.get('access')

        response = Response({"detail": "Token refreshed","access": acess},status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token',
            value=acess,
            httponly=True,
            secure=True,
            samesite='Lax',
        )

        return response


class LogoutView(APIView):

    """
    View for user logout.
    
    Permissions:
        IsAuthenticated: Only authenticated users can log out.

    POST:
        Receives: No body required, uses token from HttpOnly cookie.
        Returns: Blacklists the refresh token, deletes 'access' and 'refresh' cookies, and returns a success message.
    """
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            return Response({"detail": "Refresh token not provided."},status=status.HTTP_400_BAD_REQUEST )
        token = RefreshToken(refresh_token)
        token.blacklist()
        print(refresh_token)
        response = Response({"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')
        return response
    

 
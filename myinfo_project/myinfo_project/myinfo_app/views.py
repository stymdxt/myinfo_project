from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.crypto import get_random_string
from myinfo.client import MyInfoPersonalClientV4
from myinfo.security import generate_code_challenge, decrypt_jwe
from myinfo.settings import (
    MYINFO_CLIENT_ID,
    MYINFO_SCOPE,
    MYINFO_DOMAIN,
    MYINFO_PURPOSE_ID,
    MYINFO_PRIVATE_KEY_SIG,
    MYINFO_PRIVATE_KEY_ENC,
)
from myinfo_app.serializers import (
    MyInfoRetrieveAccessTokenSerializer,
    MyInfoRetrieveDataSerializer,
)

class MyInfoAuthURLView(APIView):
    """
    Generates the MyInfo authorization URL to initiate the authentication flow.
    """
    def get(self, request):
        try:
            # Generate state and PKCE values
            oauth_state = get_random_string(length=16)
            code_verifier = get_random_string(length=43)
            code_challenge = generate_code_challenge(code_verifier)
            callback_url = "http://localhost:3001/callback"

            # Initialize client and generate authorization URL
            client = MyInfoPersonalClientV4(
                domain=MYINFO_DOMAIN,
                client_id=MYINFO_CLIENT_ID,
                scope=MYINFO_SCOPE,
                purpose_id=MYINFO_PURPOSE_ID,
                private_key_sig=MYINFO_PRIVATE_KEY_SIG,
                private_key_enc=MYINFO_PRIVATE_KEY_ENC,
            )
            auth_url = client.get_authorise_url(oauth_state, callback_url, code_challenge)
            return Response({"auth_url": auth_url, "code_verifier": code_verifier})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MyInfoRetrieveAccessTokenView(APIView):
    """
    Retrieves the access token from MyInfo API using the authorization code.
    """
    def post(self, request):
        serializer = MyInfoRetrieveAccessTokenSerializer(data=request.data)
        if serializer.is_valid():
            auth_code = serializer.validated_data['auth_code']
            oauth_state = serializer.validated_data['oauth_state']
            code_verifier = serializer.validated_data['code_verifier']
            callback_url = "http://localhost:3001/callback"

            try:
                # Initialize client and retrieve access token
                client = MyInfoPersonalClientV4(
                    domain=MYINFO_DOMAIN,
                    client_id=MYINFO_CLIENT_ID,
                    scope=MYINFO_SCOPE,
                    purpose_id=MYINFO_PURPOSE_ID,
                    private_key_sig=MYINFO_PRIVATE_KEY_SIG,
                    private_key_enc=MYINFO_PRIVATE_KEY_ENC,
                )
                access_token = client.retrieve_access_token(auth_code, oauth_state, callback_url, code_verifier)
                return Response({"access_token": access_token})
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyInfoRetrieveDataView(APIView):
    """
    Retrieves user data from MyInfo API using the access token.
    """
    def post(self, request):
        serializer = MyInfoRetrieveDataSerializer(data=request.data)
        if serializer.is_valid():
            access_token = serializer.validated_data['access_token']

            try:
                # Initialize client and fetch encrypted user data
                client = MyInfoPersonalClientV4(
                    domain=MYINFO_DOMAIN,
                    client_id=MYINFO_CLIENT_ID,
                    scope=MYINFO_SCOPE,
                    purpose_id=MYINFO_PURPOSE_ID,
                    private_key_sig=MYINFO_PRIVATE_KEY_SIG,
                    private_key_enc=MYINFO_PRIVATE_KEY_ENC,
                )
                encrypted_data = client.retrieve_person_data(access_token)

                # Decrypt user data
                person_data = decrypt_jwe(encrypted_data)
                return Response(person_data)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

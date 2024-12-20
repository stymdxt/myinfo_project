from rest_framework import serializers

class MyInfoRetrieveDataSerializer(serializers.Serializer):
    auth_code = serializers.CharField(required=True)
    oauth_state = serializers.CharField(required=True)
from rest_framework import serializers

class MyInfoAuthURLSerializer(serializers.Serializer):
    """
    Serializer for generating MyInfo authorization URL.
    No input is required in this step, but you may add context-specific fields if needed.
    """
    pass  # No input validation needed for authorization URL generation


class MyInfoRetrieveAccessTokenSerializer(serializers.Serializer):
    """
    Serializer for retrieving the access token from MyInfo API.
    """
    auth_code = serializers.CharField(required=True, max_length=128)
    oauth_state = serializers.CharField(required=True, max_length=128)
    code_verifier = serializers.CharField(required=True, max_length=128)

    def validate(self, data):
        """
        Custom validation for auth_code and oauth_state.
        """
        if not data['auth_code']:
            raise serializers.ValidationError({"auth_code": "Authorization code is required."})
        if not data['oauth_state']:
            raise serializers.ValidationError({"oauth_state": "OAuth state is required."})
        if not data['code_verifier']:
            raise serializers.ValidationError({"code_verifier": "Code verifier is required for PKCE."})
        return data


class MyInfoRetrieveDataSerializer(serializers.Serializer):
    """
    Serializer for retrieving user data from MyInfo API using the access token.
    """
    access_token = serializers.CharField(required=True)

    def validate_access_token(self, value):
        """
        Custom validation for access_token.
        """
        if not value or len(value) < 20:
            raise serializers.ValidationError("Invalid access token.")
        return value

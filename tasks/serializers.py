from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super().get_token(user)
        # Puedes agregar información adicional al token si lo deseas
        # token['custom_field'] = user.custom_field
        return token

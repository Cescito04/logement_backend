from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class TokenResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'nom_utilisateur', 'email', 'telephone', 'cni', 'role', 'password', 'cree_le')
        read_only_fields = ('id', 'cree_le')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Cet email est déjà utilisé.')
        return value

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Email ou mot de passe invalide.')
        if not user.is_active:
            raise serializers.ValidationError('Ce compte est désactivé.')
        data['user'] = user
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nom_utilisateur', 'email', 'telephone', 'cni', 'role', 'cree_le')
        read_only_fields = ('id', 'email', 'cree_le', 'role') 
from rest_framework import serializers

from .models import * 
from django.contrib.auth import get_user_model 
User = get_user_model()

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField()

    name_rol = serializers.CharField(source="role.name", read_only=True)
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password', None)
        return ret


class RegisterSerializer(serializers.ModelSerializer):
    
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'birthday','role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role', None)

        user = User.objects.create_user(**validated_data)

        # Asignar el rol al usuario
        if role:
            user.role = role
        
        user.save()
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    name_rol = serializers.CharField(source="role.name", read_only=True)
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'date_joined',
            'birthday',
            'username',
            'role',  # Asegúrate de agregar 'role' aquí
            'name_rol'
        ]



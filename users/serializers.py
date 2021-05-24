from rest_framework import serializers

from users.models import NetworkUser


class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(read_only=True)
    link = serializers.HyperlinkedIdentityField(view_name='user_detail')

    class Meta:
        model = NetworkUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'avatar', 'last_login', 'link'
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField()

    class Meta:
        model = NetworkUser
        fields = [
            'email', 'first_name', 'last_name', 'password', 'password_confirm'
        ]

    def save(self, *args, **kwargs):
        user = NetworkUser(email=self.validated_data['email'],
                           first_name=self.validated_data['first_name'],
                           last_name=self.validated_data['last_name'])
        password = self.validated_data['password']
        password_confirm = self.validated_data['password_confirm']
        if password != password_confirm:
            raise serializers.ValidationError({'password': 'Passwords do not match '})
        user.set_password(password)
        user.save()
        return user

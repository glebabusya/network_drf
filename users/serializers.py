from rest_framework import serializers

from users.models import NetworkUser


class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(read_only=True)
    link = serializers.HyperlinkedIdentityField(view_name='user_detail')
    add_friend = serializers.HyperlinkedIdentityField(view_name='add_friend', lookup_field='id')
    friend = serializers.HyperlinkedRelatedField(view_name='user_detail', read_only=True, many=True)
    lose_friend = serializers.HyperlinkedIdentityField(view_name='lose_friend', lookup_field='id')

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        request = self.context.get("request")
        if not request.user.is_authenticated:
            data.pop('lose_friend')
            return data
        user = request.user
        if instance.id == user.id:
            data.pop('add_friend')
            data.pop('lose_friend')
            return data
        try:
            user.friend.get(id=instance.id)
            data.pop('add_friend')
        except NetworkUser.DoesNotExist:
            data.pop('lose_friend')
        return data

    class Meta:
        model = NetworkUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'avatar',
            'last_login', 'link', 'friend', 'add_friend', 'lose_friend'
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

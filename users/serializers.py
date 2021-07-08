from rest_framework import serializers
from users.models import NetworkUser


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserSerializer(DynamicFieldsModelSerializer):
    last_login = serializers.DateTimeField(read_only=True)
    link = serializers.HyperlinkedIdentityField(view_name='user_detail')
    add_friend = serializers.HyperlinkedIdentityField(view_name='add_friend', lookup_field='id')
    friends = serializers.HyperlinkedRelatedField(view_name='user_detail', read_only=True, many=True)
    lose_friend = serializers.HyperlinkedIdentityField(view_name='lose_friend', lookup_field='id')
    common_friends = serializers.SerializerMethodField('get_common_friends')
    notes = serializers.HyperlinkedRelatedField(view_name='note_detail', read_only=True, many=True)
    comments = serializers.HyperlinkedRelatedField(view_name='comment_detail', read_only=True, many=True)
    communities = serializers.HyperlinkedRelatedField(view_name='community_detail', read_only=True,
                                                      many=True, lookup_field='slug')

    def get_common_friends(self, instance):
        request = self.context['request']
        if request.user.is_authenticated:
            common_friends = instance.common_friends(request.user.id)
            fields = ('link', 'add_friend', 'lose_friend')
            return UserSerializer(common_friends, context={'request': request}, many=True, fields=fields).data

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        request = self.context.get("request")
        if not request.user.is_authenticated:
            data.pop('common_friends')
            data.pop('lose_friend')
            return data
        user = request.user
        if instance.id == user.id:
            data.pop('add_friend')
            data.pop('lose_friend')
            data.pop('common_friends')
            return data
        try:
            user.friends.get(id=instance.id)
            data.pop('add_friend')
        except NetworkUser.DoesNotExist:
            data.pop('lose_friend')
            if user.closed:
                data.pop('communities')
        return data

    class Meta:
        model = NetworkUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'avatar', 'notes', 'comments', 'communities',
            'last_login', 'link', 'common_friends', 'friends', 'add_friend', 'lose_friend', 'closed'
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

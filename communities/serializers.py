from rest_framework import serializers
import communities
from users.models import NetworkUser
from .models import Community


class CommunitySerializer(serializers.ModelSerializer):
    subscribers = serializers.HyperlinkedRelatedField(read_only=True, view_name='user_detail', many=True)
    admin = serializers.HyperlinkedRelatedField(read_only=True, view_name='user_detail', )
    staff = serializers.HyperlinkedRelatedField(read_only=True, view_name='user_detail', many=True)
    link = serializers.HyperlinkedIdentityField(read_only=True, view_name='community_detail', lookup_field='slug')
    subscribe = serializers.HyperlinkedIdentityField(view_name='subscribe', lookup_field='slug')
    unsubscribe = serializers.HyperlinkedIdentityField(view_name='unsubscribe', lookup_field='slug')

    class Meta:
        model = Community
        fields = ['slug',
                  'title',
                  'description',
                  'avatar',
                  'closed',
                  'subscribers',
                  'created_at',
                  'link',
                  'admin',
                  'staff',
                  'subscribe',
                  'unsubscribe',
                  ]

    def to_representation(self, instance):
        data = super(CommunitySerializer, self).to_representation(instance)
        request = self.context.get('request')

        if not instance.staff.filter(id=request.user.id).exists():
            data.pop('admin')
            data.pop('staff')
        else:
            data.pop('subscribe')
            data.pop('unsubscribe')
            return data

        if instance.subscribers.filter(id=request.user.id).exists():
            data.pop('subscribe')
        else:
            data.pop('unsubscribe')
        return data

    def __init__(self, *args, **kwargs):
        view = kwargs.get('context').get('view')
        super(CommunitySerializer, self).__init__(*args, **kwargs)

        if self.instance is None:
            self.fields.pop('staff')

        elif isinstance(view, communities.views.CommunityDetailAPIView):
            if self.instance.admin == self.context['request'].user:
                staff = self.instance.subscribers.exclude(id__in=self.instance.staff.all())
                if staff.count():
                    self.fields['add_staff'] = serializers.PrimaryKeyRelatedField(queryset=staff,
                                                                                  write_only=True)

    def update(self, instance, validated_data):
        instance.slug = validated_data.get('slug', instance.slug)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.closed = validated_data.get('closed', instance.closed)
        try:
            user = NetworkUser.objects.get(email=validated_data.get('staff'))
            instance.staff.add(user)
        except NetworkUser.DoesNotExist:
            pass
        instance.save()
        return instance

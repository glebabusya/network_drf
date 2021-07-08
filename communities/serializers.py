from rest_framework import serializers
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
                  'unsubscribe']

    def create(self, validated_data):
        request = self.context.get('request')

        community = Community(slug=validated_data['slug'],
                              title=validated_data['title'],
                              description=validated_data['description'],
                              avatar=validated_data['avatar'],
                              closed=validated_data['closed'],
                              admin=request.user)
        community.save()
        community.staff.add(request.user)
        community.subscribers.add(request.user)
        community.save()
        return community

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

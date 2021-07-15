from django.shortcuts import redirect
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.views import APIView
from .models import Community, SubscribeRequest
from .serializers import CommunitySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsStaffOrReadOnly


class CommunityListAPIView(ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)


class CommunityDetailAPIView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsStaffOrReadOnly]


class Subscribe(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        community = get_object_or_404(Community, slug=slug)
        if community.subscribers.filter(id=request.user.id).exists():
            return redirect('community_detail', slug)
        community.subscribe(request.user.id)

        return redirect('community_detail', slug)


class UnSubscribe(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        community = get_object_or_404(Community, slug=slug)
        if not community.subscribers.filter(id=request.user.id).exists():
            return redirect('community_detail', slug)

        subscribe_request = SubscribeRequest.objects.filter(sender=request.user, receiver=community)

        if community.closed and subscribe_request.exists():
            subscribe_request[0].delete()
        else:
            community.subscribers.remove(request.user)

        return redirect('community_detail', slug)
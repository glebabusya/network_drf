from django.shortcuts import redirect
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import NetworkUser, FriendRequest
from .serializers import UserPublicSerializer, UserRegistrationSerializer, UserCloseSerializer
from .permissions import IsOwnerOrReadOnly, IsNotAuthenticated, IsOpenOrFriend


class UserListAPIView(ListAPIView):
    queryset = NetworkUser.objects.all()
    lookup_field = 'id'
    serializer_class = UserCloseSerializer


class UserDetailAPIView(RetrieveUpdateAPIView):
    queryset = NetworkUser.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        user = get_object_or_404(NetworkUser, pk=int(self.kwargs.get('pk')))
        if user.closed:
            if not user.friends.filter(id=self.request.user.id).exists():
                return UserCloseSerializer
        return UserPublicSerializer


class UserRegistrationAPIView(CreateAPIView):
    queryset = NetworkUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return redirect('user_list')
        else:
            data = serializer.errors
            return Response(data)


class AddFriend(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        friend = get_object_or_404(NetworkUser, id=id)
        if friend == request.user:
            return redirect('user_detail', id)
        friend_request = FriendRequest.objects.filter(sender=friend, receiver=request.user)
        if friend_request.exists():
            friend_request[0].accept()
        else:
            obj, created = FriendRequest.objects.get_or_create(sender=request.user, receiver=friend)
        return redirect('user_detail', id)


class LoseFriend(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = request.user
        friend = get_object_or_404(NetworkUser, id=id)
        if user.id == friend.id:
            return redirect('user_detail', id)
        user.friends.remove(friend)
        friend.friends.remove(user)
        user.save()
        friend.save()
        return redirect('user_detail', id)


class FriendListAPIView(ListAPIView):
    permission_classes = [IsOpenOrFriend]
    serializer_class = UserCloseSerializer

    def get_queryset(self):
        return get_object_or_404(NetworkUser, pk=self.kwargs.get('pk')).friends.all()

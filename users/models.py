from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Q

from .managers import NetworkUserManager


class NetworkUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    avatar = models.ImageField(upload_to='users', null=True, blank=True)
    objects = NetworkUserManager()
    USERNAME_FIELD = 'email'
    closed = models.BooleanField(default=False)

    friends = models.ManyToManyField(to='self',
                                     related_name='friends',
                                     blank=True)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    def common_friends(self, friend_id):
        friend_friends = self.__class__.objects.get(id=friend_id).friends.exclude(id=self.id)
        my_friends = self.friends.exclude(id=friend_id)
        common_friends = self.friends.filter(Q(id__in=friend_friends) & Q(id__in=my_friends))
        return common_friends


class FriendRequest(models.Model):
    sender = models.ForeignKey(NetworkUser, on_delete=models.CASCADE,
                               related_name='friend_request_from', null=True, blank=True)
    receiver = models.ForeignKey(NetworkUser, on_delete=models.CASCADE,
                                 related_name='friend_request_to', null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True, null=True)

    def accept(self):
        user = self.sender
        friend = self.receiver
        user.friends.add(friend)
        friend.friends.add(user)
        user.save()
        friend.save()
        self.delete()

    def decline(self):
        self.delete()

    def __str__(self):
        return f'from {self.sender} to {self.receiver}'

from django.db import models

from users.models import NetworkUser


class Community(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    admin = models.ForeignKey(to=NetworkUser, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=30, null=True)
    description = models.TextField(blank=True)
    subscribers = models.ManyToManyField(to=NetworkUser, related_name='communities', blank=True)
    avatar = models.ImageField(upload_to='communities', null=True, blank=True)
    closed = models.BooleanField(default=False)
    chat = models.BooleanField(default=False)
    staff = models.ManyToManyField(to=NetworkUser, related_name='staff', blank=True)

    def __str__(self):
        return self.title

    def subscribe(self, user):
        if not self.closed:
            self.subscribers.add(user)
        else:
            subscribe_request = SubscribeRequest(user, self)
            subscribe_request.save()


class SubscribeRequest(models.Model):
    sender = models.ForeignKey(NetworkUser, on_delete=models.CASCADE,
                               related_name='subscribe_request_from', null=True, blank=True)
    receiver = models.ForeignKey(Community, on_delete=models.CASCADE,
                                 related_name='subscribe_request_to', null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True, null=True)

    def accept(self):
        user = self.sender
        community = self.receiver
        community.subscribers.add(user)
        self.delete()

    def decline(self):
        self.delete()

    def __str__(self):
        return f'from {self.sender} to {self.receiver}'

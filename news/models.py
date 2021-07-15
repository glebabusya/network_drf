from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Note(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to='notes', blank=True)
    uploaded_time = models.DateTimeField(auto_now_add=True, null=True)
    can_be_commented = models.BooleanField(default=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, blank=True, null=True)
    object_id = models.PositiveIntegerField(default=1)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.text

    @classmethod
    def get_notes_can_be_comment(cls, user):
        notes = cls.objects.all()
        notes_list = []
        for note in notes:
            if note.can_be_commented:
                if note.content_object.closed:
                    if note.content_object.friends.filter(id=user.id):
                        notes_list.append(note)
                else:
                    notes_list.append(note)
        return notes_list


class Comment(models.Model):
    text = models.CharField(max_length=200)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True, related_name='comments',
                               on_delete=models.CASCADE)
    note = models.ForeignKey(to=Note, blank=True, null=True, related_name='comments', on_delete=models.CASCADE)
    uploaded_time = models.DateTimeField(auto_now_add=True, null=True)
    comment = models.ForeignKey(to='self', blank=True, null=True, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    @classmethod
    def get_comments_can_be_comment(cls, user):
        comments = cls.objects.all()
        comments_list = []
        for comment in comments:
            if comment.note.can_be_commented:
                if comment.note.content_object.closed:
                    if comment.note.content_object.friends.filter(id=user.id):
                        comments_list.append(comment)
                else:
                    comments_list.append(comment)
        return comments_list

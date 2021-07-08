from rest_framework import serializers
from . import models
from .models import Note, Comment


class NoteSerializer(serializers.ModelSerializer):
    author = serializers.HyperlinkedRelatedField(view_name='user_detail', read_only=True)
    comments = serializers.HyperlinkedRelatedField(view_name='comment_detail', read_only=True, many=True)

    class Meta:
        model = models.Note
        fields = ['text', 'image', 'author', 'uploaded_time', 'comments']


class CommentSerializer(serializers.ModelSerializer):

    to = serializers.ChoiceField(choices=[], write_only=True)
    comment = serializers.HyperlinkedRelatedField(view_name='comment_detail', read_only=True)
    author = serializers.HyperlinkedRelatedField(view_name='user_detail', read_only=True)
    note = serializers.HyperlinkedRelatedField(view_name='note_detail', read_only=True)

    class Meta:
        model = models.Comment
        fields = ['text', 'author', 'note', 'comment', 'uploaded_time', 'to']

    def save(self, *args, **kwargs):
        to = self.validated_data['to']
        request = self.context.get('request')
        if 'note' in to:
            note = Note.objects.get(id=int(to[5:]))
            parent_comment = None
        else:
            parent_comment = Comment.objects.get(id=int(to[8:]))
            note = Note.objects.get(comments=parent_comment)
        comment = Comment(text=self.validated_data['text'],
                          note=note,
                          author=request.user,
                          comment=parent_comment)
        comment.save()
        return comment

    def __init__(self, *args, **kwargs):

        super(CommentSerializer, self).__init__(*args, **kwargs)

        NOTES_CHOICES = [('note' + str(note.id), str(note.text)) for note
                         in Note.get_notes_can_be_comment(self.context['request'].user)]
        COMMENTS_CHOICES = [('comment' + str(comment.id), str(comment.text)) for comment
                            in Comment.get_comments_can_be_comment(self.context['request'].user)]
        TO_CHOICES = [
            ('Note', NOTES_CHOICES),
            ('Comment', COMMENTS_CHOICES)
        ]
        self.fields['to'] = serializers.ChoiceField(choices=TO_CHOICES, write_only=True)
        if self.instance is not None:
            self.fields.pop('to')
        print(self.context['request'])

from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .models import Post, Comment, Tag
from taggit.forms import TagWidget

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # ✅ include tags
        widgets = {
            'tags': TagWidget(attrs={'placeholder': 'Add tags separated by commas'}),  # ✅ correct usage
        }

    class Meta:
        model = Post
        fields = ['title', 'content']  # tags handled separately via tag_field

    def __init__(self, *args, **kwargs):
        # If instance provided, populate tag_field with existing tags
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if instance and instance.pk:
            tags_qs = instance.tags.all()
            if tags_qs.exists():
                names = ', '.join([t.name for t in tags_qs])
                self.fields['tag_field'].initial = names

    def save(self, commit=True, user=None):
        # Save post first (without tags)
        post = super().save(commit=False)
        if user and not post.pk:
            post.author = user
        if commit:
            post.save()
        # handle tag_field: split, strip, create if necessary, attach
        tag_text = self.cleaned_data.get('tag_field', '')
        tag_names = [t.strip() for t in tag_text.split(',') if t.strip()]
        # get or create tag objects
        tags = []
        for name in tag_names:
            tag_obj, _ = Tag.objects.get_or_create(name__iexact=name, defaults={'name': name}) \
                         if False else Tag.objects.get_or_create(name=name)
            tags.append(tag_obj)
        # assign tags (many-to-many relationship)
        if commit:
            post.tags.set(tags)
        else:
            # If not commit, store tags to set later
            post._pending_tags = tags
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write a comment...'}),
        }

    def clean_content(self):
        data = self.cleaned_data.get('content', '').strip()
        if not data:
            raise forms.ValidationError("Comment cannot be empty.")
        return data        

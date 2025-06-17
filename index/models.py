from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Question(models.Model):
    questionTitle = models.TextField()
    questionViews = models.BigIntegerField(default=0)
    ip = models.GenericIPAddressField(null=True)
    slug = models.SlugField(null=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.questionTitle)

    def get_absolute_url(self):
        return reverse('question', args=[str(self.id), self.slug])

class Verified(models.Model):
    fullName = models.CharField(max_length=255)
    aboutUser = models.URLField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullName

class Comment(models.Model):
    questionId = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="comments")
    verifiedUser = models.ForeignKey(Verified, on_delete=models.CASCADE, related_name="verification", default=1, null=True)
    commentText = models.TextField()
    ip = models.GenericIPAddressField(null=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.commentText

class BlockedIP(models.Model):
    ip = models.GenericIPAddressField()

    def __str__(self):
        return str(self.ip)

from django.db import models
from django.contrib.auth.models import User

from utils import get_file_path


class Group(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Circle(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.FileField(upload_to=get_file_path, blank=True)
    owner = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    permission = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return r'%s create %s on %s' % (self.owner.username,
                                        self.name,
                                        self.date)


class UserCircle(models.Model):
    user = models.ForeignKey(User)
    circle = models.ForeignKey(Circle)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return r'%s joined %s on %s' % (self.user.username,
                                        self.circle.name,
                                        self.date)


class Topic(models.Model):
    circle = models.ForeignKey(Circle, related_name="topics")
    author = models.ForeignKey(User)
    text = models.TextField()
    permission = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return r'%s created %s on %s in %s' % (self.author.username,
                                               self.text[:30],
                                               self.date,
                                               self.circle.name)


class TopicComment(models.Model):
    topic = models.ForeignKey(Topic, related_name="replies")
    author = models.ForeignKey(User)
    text = models.TextField()
    permission = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return r'%s commented %s on %s in %s' % (self.author.username,
                                                 self.text[:30],
                                                 self.date,
                                                 self.topic.text[:30])

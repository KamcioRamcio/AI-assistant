from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class TodoList(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todo_lists', null=True, blank=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Todo(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.TextField()
    deadline = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    todo_list = models.ForeignKey(
        TodoList,
        on_delete=models.CASCADE,
        related_name='todos',
        default=1
    )
    def __str__(self):
        return self.task


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    TASK_STATES = [
        ('NAME', 'Waiting for task name'),
        ('DEADLINE', 'Waiting for deadline'),
        ('LOCATION', 'Waiting for location'),
        (None, 'No active task')
    ]
    task_state = models.CharField(max_length=8, choices=TASK_STATES, null=True, blank=True)
    task_name = models.CharField(max_length=255, null=True, blank=True)
    task_deadline = models.DateField(null=True, blank=True)
    task_location = models.CharField(max_length=255, null=True, blank=True)
    TODO_LIST_STATES = [
        ('ID', 'Waiting for todo list ID'),
        (None, 'No active todo list')
    ]
    todo_list_state = models.CharField(max_length=2, choices=TODO_LIST_STATES, null=True, blank=True)
    todo_list_id = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return f"Conversation {self.id} - {self.created_at}"

class Message(models.Model):
    SENDER_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]

    id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.sender.capitalize()} at {self.timestamp}: {self.content[:30]}"


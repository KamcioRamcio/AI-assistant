from rest_framework import serializers
from .models import Todo, Conversation, User, Message, TodoList



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

class TodoSerializer(serializers.ModelSerializer):
    todo_list_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Todo
        fields = ['id', 'task', 'deadline', 'location', 'is_completed', 'todo_list', 'todo_list_id']

class TodoListSerializer(serializers.ModelSerializer):
    todos = TodoSerializer(many=True, read_only=True)

    class Meta:
        model = TodoList
        fields = ['id', 'name', 'created_at', 'todos']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email')  # New field
    message_count = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'user_email', 'created_at', 'message_count', 'messages']

    def get_message_count(self, obj):
        return obj.messages.count()

    def get_messages(self, obj):
        return [
            {
                "id": msg.id,
                "content": msg.content,
                "sender": msg.sender,
                "timestamp": msg.timestamp
            }
            for msg in obj.messages.all().order_by('timestamp')
        ]
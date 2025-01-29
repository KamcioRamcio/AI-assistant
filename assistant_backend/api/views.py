from rest_framework.exceptions import PermissionDenied
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from . import serializers
from .models import Todo, Conversation, Message, User, TodoList
from .serializers import TodoSerializer, ConversationSerializer, UserSerializer, TodoListSerializer, MessageSerializer
from .logic.chat_logic import HandleQuery
from .logic._logic import Event
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
import logging

from .services.todo_service import TodoService

logger = logging.getLogger(__name__)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data['password'])
        user.save()

class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=400)

        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': f'Bearer {token.key}',
                'username': user.username,
                'user_id': user.id
            }, status=200)

        logger.warning(f'Invalid login attempt for username: {username}')
        return Response({'error': 'Invalid credentials'}, status=401)
class TodoListCreateView(generics.ListCreateAPIView):
    serializer_class = TodoListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TodoList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# views.py
class TodoCreateView(generics.CreateAPIView):
    serializer_class = TodoSerializer
    # TODO
    #   resolve the issue with Unathorized access when adding task via _logic.py
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(todo_list_id=self.request.data.get('todo_list_id'))



class UserTodosView(generics.ListAPIView):
    serializer_class = TodoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(todo_list__user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'todos': serializer.data})
class TodoUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = TodoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(todo_list__user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.todo_list.user != self.request.user:
            raise PermissionDenied("You don't own this todo item")
        serializer.save(is_completed=self.request.data.get('is_completed', serializer.instance.is_completed))


class HandleQueryView(APIView):
    serializer_class = ConversationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            query = data.get('query', '').strip()

            if not query:
                return Response({'error': 'Query is required'}, status=400)

            conversation_id = data.get('conversation_id')

            if conversation_id:
                conversation = Conversation.objects.get(id=conversation_id, user=request.user)
            else:
                conversation = Conversation.objects.create(user=request.user)

            Message.objects.create(
                conversation=conversation,
                sender='user',
                content=query
            )

            handler = HandleQuery(query, conversation_id=conversation.id, conversation=conversation)
            response_text = handler.get_response()

            Message.objects.create(
                conversation=conversation,
                sender='assistant',
                content=response_text
            )

            return Response({
                'response': response_text,
                'conversation_id': conversation.id
            })


        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON format'}, status=400)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=404)
        except Exception as e:
            logger.error(f"Error in HandleQueryView: {str(e)}")
            return Response({'error': 'Internal server error'}, status=500)

class ConversationDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id, user=request.user)
            serializer = ConversationSerializer(conversation)
            return Response(serializer.data, status=200)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=404)


class UserConversationsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        conversations = Conversation.objects.filter(user=request.user)
        serializer = ConversationSerializer(conversations, many=True)

        return Response({'conversations': serializer.data})

class OllamaProcessView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id, user=request.user)
            # Process the conversation with Ollama
            ollama_response = self.process_with_ollama(conversation)
            return Response({'ollama_response': ollama_response}, status=200)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=404)

    def process_with_ollama(self, conversation):
        # Implement the logic to process the conversation with Ollama
        # This is a placeholder function and should be replaced with actual logic
        return f"Processed conversation {conversation.id} with Ollama"

class CalendarView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        handler = Event()
        response = handler.get_outside_events()
        return Response(response)
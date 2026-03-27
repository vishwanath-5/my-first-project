from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer

# GET all tasks + POST new task
from rest_framework.permissions import IsAuthenticated
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# GET single task + UPDATE + DELETE
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if User.objects.filter(username=username).exists():
        return Response({"error":"User already exists"}, status=400)
    user = User.objects.create_user(username=username, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})

from django.contrib.auth import authenticate

@api_view(['POST'])
def login(request):
    user = authenticate(
        username=request.data.get("username"),
        password=request.data.get("password")
    )
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
    return Response({"error" : "Invalid credentials"}, status=400)
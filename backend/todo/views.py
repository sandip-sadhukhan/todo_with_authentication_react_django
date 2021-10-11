from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer


class TodoListView(APIView):
    """
    return all the todos of a perticular user
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        todos = Todo.objects.filter(user=request.user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            body = serializer.data['body']
            todo = Todo.objects.create(user=request.user, body=body)
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetailView(APIView):
    """
    crud operation on todo
    """
    permission_classes = (IsAuthenticated,)

    def get_todo(self, request, id):
        try:
            return Todo.objects.get(id=id, user=request.user)
        except Todo.DoesNotExist:
            raise Http404

    def get(self, request, id):
        todo = self.get_todo(request, id)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def put(self, request, id):
        todo = self.get_todo(request, id)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        todo = self.get_todo(request, id)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    category = request.query_params.get('category')
    if category:
        tasks = tasks.filter(category=category)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(
            {'error': 'Task not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = TaskSerializer(task)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_create(request):
    if request.user.role != 'poster':
        return Response(
            {'error': 'Only posters can create tasks'},
            status=status.HTTP_403_FORBIDDEN
        )
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(poster=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_tasks(request):
    tasks = Task.objects.filter(
        poster=request.user
    ).order_by('-created_at')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def task_update_status(request, pk):
    try:
        task = Task.objects.get(pk=pk, poster=request.user)
    except Task.DoesNotExist:
        return Response(
            {'error': 'Task not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    new_status = request.data.get('status')
    if new_status not in ['open', 'assigned', 'completed', 'cancelled']:
        return Response(
            {'error': 'Invalid status'},
            status=status.HTTP_400_BAD_REQUEST
        )
    task.status = new_status
    task.save()
    return Response(TaskSerializer(task).data)
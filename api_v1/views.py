import json

from django.http import JsonResponse, Http404

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from issue_tracker.models import Project, Task
from api_v1.serializer import ProjectSerializer, TaskSerializer


class ApiProjectListView(APIView):
    def get(self, request, *args, **kwargs):
        objects = Project.objects.all()
        serializer = ProjectSerializer(objects, many=True)
        return JsonResponse(serializer.data, safe=False)


class ApiProjectView(APIView):
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return JsonResponse(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        data = json.loads(request.body)
        serializer = ProjectSerializer(project, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            response = JsonResponse({'errors': serializer.errors})
            response.status_code = 400
            return response

    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return JsonResponse({'deleted project pk': project.pk})


class ApiTaskListView(APIView):
    def get(self, request, *args, **kwargs):
        objects = Task.objects.all()
        serializer = TaskSerializer(objects, many=True)
        return JsonResponse(serializer.data, safe=False)


class ApiTaskView(APIView):
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return JsonResponse(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        task = self.get_object(pk)
        task_body = json.loads(request.body)
        serializer = TaskSerializer(task, data=task_body)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            response = JsonResponse({'errors': serializer.errors})
            response.status_code = 400
            return response

    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        return JsonResponse({'deleted task pk': task.pk})

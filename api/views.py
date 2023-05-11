from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer

from .models import Task

import openai

# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
		"List':'/task-list/",
		"Detail View':'/task-detail/<str:pk>/",
		"Create':'/task-create/",
		"Update':'/task-update/<str:pk>/",
		"Delete':'/task-delete/<str:pk>/",
		"Assist':'/task-assist/<str:pk>/",
		}
    
    return Response(api_urls)

@api_view(['GET'])
def taskList(request):
	tasks = Task.objects.all().order_by('-id')
	serializer = TaskSerializer(tasks, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def taskDetail(request, pk):
	tasks = Task.objects.get(id=pk)
	serializer = TaskSerializer(tasks, many=False)
	return Response(serializer.data)

@api_view(['POST'])
def taskCreate(request):
	serializer = TaskSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
def taskUpdate(request, pk):
	task = Task.objects.get(id=pk)
	serializer = TaskSerializer(instance=task, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
def taskDelete(request, pk):
	task = Task.objects.get(id=pk)
	task.delete()

	return Response('Item succsesfully deleted!')


@api_view(['POST'])
def taskAssist(request, pk):

	title = Task.objects.get(id=pk)

	# OPENAI CHAT COMPLETION

	openai.api_key = ""

	messages = [{"role": "system", "content": f'You are a helpful assistant. You happily work for a person with a todo list. You provide helpful insight for the items on the todo list when the person requests your help. You do this in 100 words for less. The person will only provide you with the content of a single item on the todo list.\n\n{title}'}]
	response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
	advice = response["choices"][0]["message"]["content"]

	task = Task.objects.get(id=pk)
	task.advice = advice
	# print(task)
	task.save()

    # return a response to the client
	return JsonResponse({'message': 'Data saved successfully'})
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import generics
from courses.models import Subject, Course
from courses.api.serializers import SubjectSerializer


# retrieving the serialzed data only
class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# showing a single api data or object 
class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# Creating a custom view(APIVIEW)
class CourseEnrollView(APIView):
    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        course.students.add(request.user)
        return Response({'enrolled': True})

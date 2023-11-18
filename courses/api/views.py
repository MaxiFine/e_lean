from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication  # for authentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics, viewsets  # viewsets for crud ops
from courses.models import Subject, Course
from courses.api.serializers import SubjectSerializer, CourseSerializer


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
    # api authentication configs using BasicAuthentication
    authentication_classes = [BaseAuthentication]  # using django base64 for auths
    permission_classes = [IsAuthenticated]  # permissions for users

    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        course.students.add(request.user)  # to add the student being enrolled
        return Response({'enrolled': True})


# Using Viewsets for course model
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
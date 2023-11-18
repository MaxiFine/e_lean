from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication  # for authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

# customizing the auth method
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User  # Import your User model
from rest_framework.authtoken.models import Token  # Import the Token model

from rest_framework import generics, viewsets  # viewsets for crud ops
from courses.models import Subject, Course
from courses.api.serializers import SubjectSerializer, CourseSerializer
from courses.api.permissions import IsEnrolled
from courses.api.serializers import CourseWithContentsSerializer

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


# Customizing authentication method
class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Your authentication logic here
        # For example, you can check for a token_header in the request header
        token_header = request.headers.get('Authorization')

        if not token_header or not token_header.startswith('Token '):
            return None

        # Add your authentication logic here, validate the token_header, and retrieve the user
        # If authentication is successful, return a two-tuple of (user, auth)
        # If authentication fails, raise AuthenticationFailed exception

        # Example:
        try:
            key = token_header.split(' ')[1]
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token_header')

        # Add your logic to retrieve the user associated with the token_header
        user = token.user

        return (user, token)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    # Use your custom authentication class
    authentication_classes = [TokenAuthentication]  # to overide auth method
    permission_classes = [IsAuthenticated]  # You can adjust this based on your requirements

    # Your other actions go here

    @action(detail=True, methods=['post'])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})

    @action(detail=True, methods=['get'], serializer_class=CourseWithContentsSerializer)
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)



# # Using Viewsets for course model
# class CourseViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer

#     # adding actions to viewsets
#     @action(detail=True, methods=['post'],
#             authentication_classes=[BaseAuthentication],
#             permission_classes=[IsAuthenticated],)
    
#     def enroll(self, request, *args, **kwargs):
#         course = self.get_object()
#         course.students.add(request.user)
#         return Response({'enrolled': True})
    
#     @action(detail=True,
#                 methods=['get'], serializer_class=CourseWithContentsSerializer,
#                 authentication_classes=[BaseAuthentication],
#                 permission_classes=[IsAuthenticated, IsEnrolled])

#     def contents(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    


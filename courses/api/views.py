from rest_framework import generics
from courses.models import Subject
from courses.api.serializers import SubjectSerializer


# retrieving the serialzed data only
class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# showing a single api data or object 
class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


from rest_framework import serializers

from courses.models import Subject, Course, Module



class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']


# serializing the module model
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['owner', 'title', 'description']


# Creating a nested serializer
class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = [
            'id', 'subject', 'title',
            'slug', 'overview', 'created', 
            'owner', 'modules',
        ]



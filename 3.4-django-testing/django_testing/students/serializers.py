from rest_framework import serializers
from .models import Course, Student
from django.conf import settings


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'birth_date']


class CourseSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Student.objects.all(),
        required=False
    )

    class Meta:
        model = Course
        fields = ['id', 'name', 'students']

    def validate_students(self, value):
        if self.instance:
            max_students = getattr(settings, 'MAX_STUDENTS_PER_COURSE', 20)
            current_students_count = self.instance.students.count()

            current_students_ids = set(self.instance.students.values_list('id', flat=True))
            new_students_ids = set(value)

            added_students = new_students_ids - current_students_ids

            if current_students_count + len(added_students) > max_students:
                raise serializers.ValidationError(
                    f'Максимальное количество студентов на курсе: {max_students}. '
                    f'Текущее количество: {current_students_count}, '
                    f'пытаетесь добавить: {len(added_students)}'
                )
        return value
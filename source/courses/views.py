from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import TemplateView, View
from accounts.models import User
from courses.models import Course
from accounts.forms import NewUserForm, LoginUserForm


class IndexPageView(TemplateView):
    template_name = 'courses/index.html'


class AboutUsView(ListView):
    model = User
    template_name = 'courses/about_us.html'
    context_object_name = 'teachers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers'] = User.objects.all().filter(role='teacher')
        return context


class CoursesView(ListView):
    model = Course
    template_name = 'courses/courses_view.html'
    context_object_name = 'courses'

class LessonsView(ListView):
    model = Lesson
    template_name = 'courses/lesson_view.html'
    context_object_name = 'lessons'
    paginate_by = 16
    paginate_orphans = 3
    ordering = ('-created_at',)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('courses', None)
        if search_query:
                queryset = queryset.filter(course__course_name__iexact=search_query)
        else:
            queryset = queryset.none()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["courses"] = Course.objects.all()
        return context
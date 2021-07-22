from django.http import HttpResponse, HttpResponseRedirect
#from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import QuestionSerializer
from .models import Question, Choice

class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            'test': 'success'
        }
        return Response(data)

    def post(self, request, *args, **kwargs):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

"""
{
"question_text": "szia",
"pub_date": "2021-07-20 12:11:44.415411"
}

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):

        Return the last five published questions (not including those set to be
        published in the future).

        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
"""

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def login(request):
   return render(request, "polls/login.html", {})

def register(request):
   return render(request, "polls/register.html", {})

"""
def login(request):
    template_name = 'polls/login.html'
    try:
        username = request.POST['username']
        password = request.POST['password']
    except (KeyError):
        return render(request, 'polls/index.html', {
            'error_message': "Wrong credentials!",
        })
    else:
        return render(request, 'polls/index.html', {
            'error_message': "Welcome!",
        })

def register(request):
    template_name = 'polls/register.html'
    try:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
    except (KeyError):
        return render(request, 'polls/index.html', {
            'error_message': "Wrong credentials!",
        })
    else:
        if password != password2:
            return render(request, 'polls/index.html', {
                'error_message': "Passwords are not the same!",
            })
        return render(request, 'polls/index.html', {
            'error_message': "Success!",
        })
"""
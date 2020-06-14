from django.shortcuts import render,get_list_or_404,get_object_or_404,reverse
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .models import Question,Choice
from django.template import loader
from django.views import generic
from django.utils import timezone
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """ 최근5개만 리턴함"""
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')[:5] 
            #__lte = less than equal
            # Question.objects.filter (pub_date__lte = timezone.now ())는 
            # timezone.now보다 pub_date가 작거나 같은 Question을 포함하는 
            # queryset을 반환합니다.
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name ='polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk= request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #질문 투표 폼을 다시 보여줌
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_message': "You didn't choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question_id, )))
        
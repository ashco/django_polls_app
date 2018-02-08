from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from .models import Question, Choice

def get_votes(choice):
    return choice.votes

def get_text(choice):
    return choice.choice_text

def index(request):
    # return HttpResponse("You're at the index page")
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(request, 'mypolls/index.html', { 'latest_question_list': latest_question_list })

def vote(request, question_id):
    # return HttpResponse("You're at the vote page")
    q = get_object_or_404(Question, pk=question_id)
    return render(request, 'mypolls/vote.html', {'question':q})

def results(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    num_values = list(map(get_votes, q.choice_set.all()))
    text_values = list(map(get_text, q.choice_set.all()))
    return render(request, 'mypolls/results.html', {
        'question': q, 
        'num_values': num_values,
        'text_values': '|'.join(text_values),
        'upper_limit': max(num_values) + max(num_values) // 10 + 1 })

def process_vote(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = q.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'mypolls/vote.html', {'question': q, 'error_message': 'You need to select a choice'})
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return redirect('/polls/{0}/results/'.format(question_id))
        #return HttpResponse("You're at the process page")
        #return HttpResponseRedirect(reverse('polls:results', args=(question_id)))

from django.shortcuts import render,get_object_or_404
from .models import Question,Choice
from .forms import PollForm
from django.http import HttpResponseRedirect,HttpRequest
from django.core.urlresolvers import reverse
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        # Return latest 10 polls 
        return Question.objects.order_by('-date')[:20]

def create(request):
    # If request method is not POST, create new form 
    form = PollForm(request.POST or None)
    if request.method == 'POST':
        
        if form.is_valid():

            que = form.cleaned_data.get('question')
            choices = form.cleaned_data.get('choices')

            choice_list = choices.split('\n')

            ques_in_db = Question(question=que)
            ques_in_db.save()

            for ch in choice_list:
                ques_in_db.choice_set.create(choice=ch)

            # Redirect to the links page of the question
            return HttpResponseRedirect(reverse('links', args=(ques_in_db.id,)))     
        
        # if form not valid return the same form with errors
    context = {
        "PollForm" : form,
    }
    return render(request,'polls/create.html',context)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answerd_ids = ""

    if 'ids' in request.COOKIES:
        answerd_ids = request.COOKIES['ids']

    print(answerd_ids)
    # Check if question id already in aswered ids
    if str(question.id) in answerd_ids.split(','):

        vote_percentage = getVotePercentage(question)
        context ={
            'question' : question,
            'vote_percentage' : vote_percentage,
            'error_message' : "You have already aswered the question.",
        }
        # Render results page for the question
        return render(request, 'polls/results.html', context)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        context = {
            'question': question,
            'error_message': "You didn't select a choice.",
        }
        return render(request, 'polls/vote.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Add question id to asnwed ids in cookie
        if answerd_ids :
            answerd_ids += ","+str(question_id)
        else :
            # Adding first id to cookie
            answerd_ids += str(question_id)
        response = HttpResponseRedirect(reverse('results', args=(question.id,)))
        response.set_cookie('ids',answerd_ids)
        
        return response


def results(request,question_id):
    question = get_object_or_404(Question, pk=question_id)

    vote_percentage = getVotePercentage(question)
    context ={
        'question' : question,
        'vote_percentage' : vote_percentage,
    }
    return render(request,'polls/results.html',context)

def links(request,question_id):
     question = get_object_or_404(Question, pk=question_id)
     hostname = request.META['HTTP_HOST']
     port = request.META['SERVER_PORT']
     url_begin = "http://"+hostname+"/polls/"+str(question_id)
     vote_url = url_begin+"/vote/"
     result_url = url_begin+"/results/"
     
     context = {
        'question' : question,
        'vote_url' : vote_url,
        'result_url' : result_url,
     }
     return render(request,'polls/links.html',context)

def getVotePercentage(question):
    total_votes = 0
    for choice in question.choice_set.all():
        total_votes += choice.votes
    
    vote_percentage = {}
    for choice in question.choice_set.all():
        per = choice.votes/total_votes*100
        vote_percentage[choice.choice] = per

    return vote_percentage
#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Candidate, Poll, Choice
from django.utils import timezone

# Create your views here.
def index(request):
    candidates = Candidate.objects.all()
    print(candidates)
    context = {'candidates': candidates}
    return render(request, 'player/index.html', context)

def player(request):
    return HttpResponse("Hello")


# def areas(request, area):
#     today = timezone.now()
#     poll = Poll.objects.get(area=area, start_date__lte=today, end_date__gte=today)
#     candidates = Candidate.objects.filter(area=area)   # 앞부분의 area는 candidate의 area
#                                                        # 뒷부분은 주소에 넣어지는 부분, 매개변수
#
#     context = {'candidates': candidates,
#                'area': area,
#                'pole': poll}
#     return render(request, 'player/area.html', context)
#
# def polls(request, poll_id):
#     poll = Poll.objects.get(pk=poll_id)
#     selection = request.POST['choice']
#
#     try:
#         choice = Choice.objects.get(poll_id = poll_id, candidate_id = selection)
#         choice.votes += 1
#         choice.save()
#
#     except:
#         choice = Choice(poll_id = poll_id, candidate_id = selection, votes=1)
#         choice.save()
#
#     return HttpResponseRedirect("/areas/{}/results".format(poll.area))
#
# def results(request, area):
#     candidates = Candidate.objects.filter(area=area)
#     polls = Poll.objects.filter(area=area)
#     poll_results = []
#     for poll in polls:
#         result = {}
#         result['start_date'] = poll.start_date
#         result['end_date'] = poll.end_date
#
#         poll_results.append(result)
#
#     context = {'candidates': candidates, 'area': area,
#                'poll_results': poll_results}
#     return render(request, 'elections/result.html', context)

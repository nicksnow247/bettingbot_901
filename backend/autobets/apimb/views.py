from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import mixins, viewsets, permissions, status
from rest_framework.views import APIView

from rest_framework.decorators import action, api_view
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from celery.signals import after_task_publish
from .models import *
from .tasks import get_events
from .serializers import (
                        EventSerializer, MarketSerializer, RunnerSerializer, BalanceSerializer, 
                        CombinedSerializer, ProfitAndLossSerializer)
from .permissions import EventPermission
from .client import get_client

class EventViewSet(mixins.ListModelMixin, 
                   mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):

    queryset = Event.objects.all().order_by('start_time')
    serializer_class = EventSerializer
    #permission_classes = (EventPermission, )

    @action(detail=False, methods=['GET'])
    def loaditem(self, request):
        api = get_client()
        sports = api.reference_data.get_sports()
        sportslist = []
        for row in sports:
            sportslist.append({'id': row['id'], 'label':row['name']})
        return Response(sportslist)

    @action(detail=False, methods=['POST'])
    def deleteitem(self, request):
        keys = request.data['keys']
        for xx in keys:
            if xx['time_key'] is None:
                if xx['event_key'] is None:
                    Event.objects.filter(sport_id=xx['sport_key']).delete()
                else:
                    Event.objects.filter(event_id=xx['event_key']).delete()
            else:
                date_str = xx['time_key']
                datetime_obj = datetime.strptime(date_str, '%d-%m-%y')
                Event.objects.filter(start_time__date=datetime_obj, sport_id=xx['sport_key']).delete()
            print(xx)
        
        return Response('request')
    
    @action(detail=False, methods=['POST'])
    def savetargetsportitem(self, request):
        SelectedSports.objects.all().delete()
        keys = request.data['keys']
        for xx in keys:
            ev, created = SelectedSports.objects.update_or_create(sport_id=xx['sport_id'])
            ev.sport_id = xx['sport_id']
            ev.sport_name = xx['sport_name']
            ev.save()
        
        return Response('request')
    
    #get_events.delay()


class MarketViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
                    
    queryset = Market.objects.all().order_by('market_name')
    serializer_class = MarketSerializer


class RunnerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Runner.objects.all()
    serializer_class = RunnerSerializer   

class BalanceViewSet(mixins.ListModelMixin, 
                    viewsets.GenericViewSet, 
                    mixins.RetrieveModelMixin):

    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer 

class CombinedViewSet(mixins.ListModelMixin, 
                    viewsets.GenericViewSet, 
                    mixins.RetrieveModelMixin):


    queryset = Runner.objects.all()
    serializer_class = CombinedSerializer

    @action(detail=False, methods=['POST'])
    def loaditem(self, request):
        keys = request.data['keys']
        queryset = []
        for xx in keys:
            if xx['time_key'] is None:
                if xx['event_key'] is None:
                    queryset.extend(Runner.objects.filter(event__sport_id=xx['sport_key']))
                else:
                    queryset.extend(Runner.objects.filter(event__event_id=xx['event_key']))
            else:
                date_str = xx['time_key']
                datetime_obj = datetime.strptime(date_str, '%d-%m-%y')
                queryset.extend(Runner.objects.filter(event__start_time__date=datetime_obj, event__sport_id=xx['sport_key']))
        
        serializer_class = CombinedSerializer(queryset, many=True)
        return Response(serializer_class.data)

    @action(detail=False, methods=['POST'])
    def saveitem(self, request):
        keys = request.data['keys']
        queryset = []
        for xx in keys:
            #
            tmp_runner = Runner.objects.filter(runner_id=xx['runner_id']).get()
            if(tmp_runner.bettriggers is None):
                tmp_trig = BetTriggers(b1_trig=xx['bettriggers']['b1_trig'],
                                       b2_trig=xx['bettriggers']['b2_trig'],
                                       l1_trig=xx['bettriggers']['l1_trig'],
                                       l2_trig=xx['bettriggers']['l2_trig'],
                                       tigger_mode=xx['bettriggers']['tigger_mode'],
                                       armbot=xx['bettriggers']['armbot'])
                tmp_trig.save()
                tmp_runner.bettriggers = tmp_trig
            else:
                tmp_trig = tmp_runner.bettriggers
                tmp_trig.b1_trig = xx['bettriggers']['b1_trig']
                tmp_trig.b2_trig = xx['bettriggers']['b2_trig']
                tmp_trig.l1_trig = xx['bettriggers']['l1_trig']
                tmp_trig.l2_trig = xx['bettriggers']['l2_trig']
                tmp_trig.tigger_mode = xx['bettriggers']['tigger_mode']
                tmp_trig.armbot = xx['bettriggers']['armbot']
                tmp_trig.save()
                tmp_runner.bettriggers = tmp_trig
            #
            if(tmp_runner.userstakes is None):
                tmp_userstake = UserStakes(back_stake=xx['userstakes']['back_stake'],
                                           lay_stake=xx['userstakes']['lay_stake'])
                tmp_userstake.save()
                tmp_runner.userstakes = tmp_userstake
            else:
                tmp_userstake = tmp_runner.userstakes
                tmp_userstake.back_stake = xx['userstakes']['back_stake']
                tmp_userstake.lay_stake = xx['userstakes']['lay_stake']
                tmp_userstake.save()
                tmp_runner.userstakes = tmp_userstake
            #
            if(tmp_runner.stakes is None):
                tmp_stake = Stakes(round_bal=xx['stakes']['round_bal'],
                                   percent_1=xx['stakes']['percent_1'],
                                   percent_2=xx['stakes']['percent_2'],
                                   percent_3=xx['stakes']['percent_3'],
                                   percent_4=xx['stakes']['percent_4'],
                                   percent_5=xx['stakes']['percent_5'],
                                   percent_6=xx['stakes']['percent_6'],
                                   percent_7=xx['stakes']['percent_7'],
                                   percent_8=xx['stakes']['percent_8'],
                                   percent_9=xx['stakes']['percent_9'],
                                   percent_10=xx['stakes']['percent_10'])
                tmp_stake.save()
                tmp_runner.stakes = tmp_stake
            else:
                tmp_stake = tmp_runner.stakes
                tmp_stake.round_bal = xx['stakes']['round_bal']
                tmp_stake.percent_1 = xx['stakes']['percent_1']
                tmp_stake.percent_2 = xx['stakes']['percent_2']
                tmp_stake.percent_3 = xx['stakes']['percent_3']
                tmp_stake.percent_4 = xx['stakes']['percent_4']
                tmp_stake.percent_5 = xx['stakes']['percent_5']
                tmp_stake.percent_6 = xx['stakes']['percent_6']
                tmp_stake.percent_7 = xx['stakes']['percent_7']
                tmp_stake.percent_8 = xx['stakes']['percent_8']
                tmp_stake.percent_9 = xx['stakes']['percent_9']
                tmp_stake.percent_10 = xx['stakes']['percent_10']
                tmp_stake.save()
                tmp_runner.stakes = tmp_stake
            #
            tmp_runner.save()
            print(tmp_runner)
            pass
        
        return Response('request')
    
class PandLViewSet(mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    queryset = ReportsMarket.objects.all().order_by('start_time')
    serializer_class = ProfitAndLossSerializer
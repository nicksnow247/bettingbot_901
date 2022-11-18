from rest_framework import serializers
from .models import *

class EventSerializer(serializers.ModelSerializer):

    start_time = serializers.DateTimeField(read_only=True, format="%d-%m-%y")
    class Meta:
        model = Event
        #fields =['sport_id','event_name','start_time','status','event_id']
        fields ='__all__'
class MarketSerializer(serializers.ModelSerializer):


    class Meta:
        model = Market
        #fields =['market_id','market_name','status','volume','event']       
        fields ='__all__'

class RunnerSerializer(serializers.ModelSerializer):


    class Meta:
        model = Runner
        #fields =['runner_id','name','back_odds','lay_odds'] 
        fields ='__all__'

class BetTriggersSerializer(serializers.ModelSerializer):
    class Meta:
        model = BetTriggers
        fields ='__all__'

class StakesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stakes
        fields ='__all__'

class UserStakesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStakes
        fields ='__all__'

class OrderStakesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields ='__all__'

class CombinedSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    market = MarketSerializer()
    bettriggers = BetTriggersSerializer()
    stakes = StakesSerializer()
    userstakes = UserStakesSerializer()
    order = OrderStakesSerializer()
    class Meta:
        model = Runner
        fields= '__all__'
       

class BalanceSerializer(serializers.ModelSerializer):


    class Meta:
        model = Balance
        fields =['id','balance','exposure','free_funds']         

class ProfitAndLossSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReportsMarket
        fields = ('id','start_time','profit_and_loss')
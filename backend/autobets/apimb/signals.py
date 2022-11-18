from __future__ import absolute_import, unicode_literals
from .tasks import *
from celery.signals import task_success, after_task_publish
from apimb.models import *
logger = logging.getLogger(__name__)


from .client import get_client
from matchbook.enums import Side

@after_task_publish.connect(sender='apimb.tasks.get_events')
def task_sent_handler(sender, body=None, **kwargs):

    runners = Runner.objects.filter(bettriggers__armbot=True, market__is_ip='True') ######### !!! need to update True
    for row in runners:
        print('&&&&&&&&&&&&&&&&&&&&')
        print(row.name)
        print(row.runner_id)
        print('&&&&&&&&&&&&&&&&&&&&')
        if row.back_odds is None:
            row.back_odds = 0
        if row.lay_odds is None:
            row.lay_odds = 0

        if(row.bettriggers.tigger_mode == 0):                   # back first
            if(row.back_odds <= row.bettriggers.b1_trig):   # back order
                trigger_order(row, 'back', True)
            elif(row.lay_odds >= row.bettriggers.l2_trig):  # lay order
                trigger_order(row, 'lay', True)
            else:
                print("nothing1")
        elif(row.bettriggers.tigger_mode == 1):                 # lay first
            if(row.lay_odds >= row.bettriggers.l1_trig):    # lay order
                trigger_order(row, 'lay', False)
            elif(row.back_odds <= row.bettriggers.b2_trig):   # back order
                trigger_order(row, 'back', False)
            else:
                print("nothing2")
        else:
            print("nothing")
            
#    print(sender)


def trigger_order(row, side, backfirst):
    api = get_client()

    if side == 'back':
        side = Side.Back
        stake = row.userstakes.lay_stake
        if backfirst:
            odds = row.bettriggers.b1_trig
        else:
            odds = row.bettriggers.b2_trig
    else:
        side = Side.Lay
        stake = row.userstakes.back_stake
        if backfirst:
            odds = row.bettriggers.l2_trig
        else:
            odds = row.bettriggers.l1_trig

    #stake = 0.1

    tmp_order = Orders.objects.filter(market_id=row.market.market_id, event_id=row.event.event_id, runner_id=row.runner_id, side=side)
    
    if len(tmp_order) == 0:
        #1307475382670017
        order_insert = api.betting.send_orders(row.runner_id, odds, side, stake)
        print(order_insert)
        pot_pro = 0
        pot_lib = 0

        if 'potential-liability' in order_insert[0]:
            pot_lib = order_insert[0]['potential-liability']
        elif 'potential-profit' in order_insert[0]:
            pot_pro = order_insert[0]['potential-profit']

        if 'remaining-potential-liability' in order_insert[0]:
            rem_pot_pro = order_insert[0]['remaining-potential-liability']
        elif 'remaining-potential-profit' in order_insert[0]:
            rem_pot_pro = order_insert[0]['remaining-potential-profit']
        else:
            rem_pot_pro = None
        tmp_order = Orders(
            temp_id = order_insert[0]['id'], # this is pk in API it's same as runner_id
            market_id = row.market.market_id,
            event_id = row.event.event_id,
            runner_id = row.runner_id,
            side = side,
            odds = odds,
            event_name = row.event.event_name,
            market_name = row.market.market_name,
            market_type = order_insert[0]['market-type'],
            runner_name = order_insert[0]['runner-name'],
            odds_type = order_insert[0]['odds-type'],
            stake = order_insert[0]['stake'],
            remaining = order_insert[0]['remaining'],
            pot_pro = pot_pro,
            pot_lib = pot_lib,
            rem_pot_pro = rem_pot_pro,
            created_at = order_insert[0]['created-at'],
            status = order_insert[0]['status'],
            inplay = order_insert[0]['in-play'],
            time_stamp = order_insert[0]['TIMESTAMP']
        )
        tmp_order.save()
        print('Created')
    else:
        tmp_obj = tmp_order.get()
        if odds != tmp_obj.odds or stake != tmp_obj.stake:
            tmp_obj.odds = odds
            tmp_obj.stake = stake
            tmp_obj.save()
            order_amend = api.betting.amend_orders(tmp_obj.temp_id, odds, side, stake)
            print('Updated')
        print('Skipped')
    #order_insert = api.betting.send_orders(row.runner_id, odds, side, 0.1)
    #order_amend = api.betting.amend_orders(order_insert[0]['id'], odds+1, side, 0.2)
    #delete_order = api.betting.delete_order(order_insert[0]['id'])
    
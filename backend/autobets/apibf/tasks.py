from client import get_betfair_client
# from sport_ids import Tennis, Soccer
from betfairlightweight import filters


trading = get_betfair_client()
event_type_id = trading.betting.list_event_types(
    filter=filters.market_filter(text_query="E-Sports")
)

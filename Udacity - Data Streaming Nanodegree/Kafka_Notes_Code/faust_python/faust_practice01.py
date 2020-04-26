import asyncio
import random
import json
from datetime import datetime, timezone
from itertools import count

import faust
from faust.cli import option


# define the data model (it doesn't have to be @dataclass)
class Withdrawal(faust.Record, isodates=True, serializer='json'):
    user: str
    country: str
    amount: float
    date: datetime = None


# Faust app
app = faust.App(
    'faust-withdrawals',
    broker="localhost:9092",
    topic_partitions=2
)

# topic
withdrawals_topic = app.topic('withdrawals', value_type=Withdrawal)

# table
user_to_total = app.Table(
    'user_to_total',
    default=int
).tumbling(3600).relative_to_stream()

# table
country_to_total = app.Table(
    'country_to_total', default=int,
).tumbling(10.0, expires=10.0).relative_to_stream()


@app.agent(withdrawals_topic)
async def track_user_withdrawal(withdrawals):
    async for withdrawal in withdrawals:
        user_to_total[withdrawal.user] += withdrawal.amount


# No topic was passed to the agent decorator, 
# so an anonymous topic will be created for it.
@app.agent()
async def track_country_withdrawal(withdrawals):
    async for withdrawal in withdrawals.group_by(withdrawals.country):
        country_to_total[withdrawal.country] += withdrawal.amount

if __name__ == '__main__':
    app.main()
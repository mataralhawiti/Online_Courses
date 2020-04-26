"""
Faust Streams
"""

import faust
from dataclasses import dataclass, asdict
import json

""" A stream is an infinite async iterable, consuming messages from a channel/topic """

@dataclass
class Purchase(faust.Record):
    username: str
    currency: str
    amount: int

app = faust.App("FaustStreams", broker="localhost:9092")
topic = app.topic(
    "com.udacity.streams.purchases",
    key_type=str,
    value_type=Purchase
)
out_topic = app.topic(
    "com.udacity.streams.purchases.high_value_international",
    key_type=str,
    value_type=Purchase,
    value_serializer="json"
)


@app.agent(topic)
async def purchase(purchases):
    async for purchase in purchases.filter(lambda x: x.currency != "USD" and x.amount > 100000):
        await out_topic.send(key=purchase.username, value=purchase)


if __name__ == "__main__":
    app.main()
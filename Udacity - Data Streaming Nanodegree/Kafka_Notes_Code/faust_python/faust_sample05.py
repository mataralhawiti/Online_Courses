"""
Faust Stream Processors and Operations

Processors : can add missing fields, change the meaning of fields, and perform any kind of desired processing.
            - Processors may execute synchronously or asynchronously within the context of your code
            - All defined processors will run, in the order they were defined, before the final value is generated.

Operations : Faust Operations are actions that can be applied to an incoming stream to create an intermediate stream 
                containing some modification, such as a group by or filter
"""



import faust

import random
from dataclasses import dataclass, asdict
import json

@dataclass
class Purchase(faust.Record):
    username: str
    currency: str
    amount: int
    fraud_score: float = 0.0

# Faust Stream Proceesro
def add_fraud_score(purchase):
    purchase.fraud_score = random.random()
    return purchase


app = faust.App("FaustStreamsProcessors", broker="localhost:9092")
topic = app.topic(
    "com.udacity.streams.purchases",
    key_type=str,
    value_type=Purchase
)
out_topic = app.topic(
    "com.udacity.streams.purchases.fraud",
    key_type=str,
    value_type=Purchase
)


@app.agent(topic)
async def purchase(purchases):
    purchases.add_processor(add_fraud_score)
    async for purchase in purchases:
        await out_topic.send(key=purchase.username, value=purchase)


if __name__ == "__main__":
    app.main()
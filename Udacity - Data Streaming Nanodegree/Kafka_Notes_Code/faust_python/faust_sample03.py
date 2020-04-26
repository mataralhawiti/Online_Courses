"""
serializing in Faust
"""

"""
Stream : is an infinite series of ordered immutable events !
"""


import faust
import json
from dataclasses import dataclass, asdict


@dataclass
class Purchase(faust.Record):
    username: str
    currency: str
    amount: str

# serilization model
@dataclass
class PurchaseDollars(faust.Record):
    username: str
    currency: str
    amount: float

# define app instance and topics
app = faust.App("SerializingFaustApp", broker="localhost:9092")
topic = app.topic(
    "com.udacity.streams.purchases",
    key_type=str,
    value_type=Purchase
)

out_tpoic = app.topic(
    "com.udacity.streams.purchases.out",
    key_type=str,
    value_type=Purchase)



# Multiple serialization codecs may be specified for a given model
# serialization=”binary|json”
@app.agent(topic)
async def purchase(purchases):
    async for purchase in purchases:
        purchase_in_dollars = PurchaseDollars(
            username=purchase.username,
            currency=purchase.currency,
            amount=purchase.amount/100.0
        )
        # write out new data to Kafak topic
        await out_tpoic.send(key=purchase.username, value=purchase_in_dollars)


if __name__ == "__main__":
    app.main()
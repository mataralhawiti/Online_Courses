"""
Windowing in Faust
Faust provides two windowing methods: hopping and tumbling. 

Windowing applies only to Tables


** Hopping  Windows **
"""


import faust
from dataclasses import dataclass, asdict
import json
from datetime import timedelta

@dataclass
class Purchase(faust.Record):
    username: str
    currency: str
    amount: int

app = faust.App("FaustTables", broker="localhost:9092")
topic = app.topic(
    "com.udacity.streams.purchases",
    key_type=str,
    value_type=Purchase
)
currency_summary_table = app.Table(
    "currency_summary",
    default=int
).hopping(
    size=timedelta(seconds=30),
    step=timedelta(seconds=5),
    expires=timedelta(minutes=10)
    
)


@app.agent(topic)
async def purchase(purchases):
    # must cco-partition (group_by)
    async for purchase in purchases.group_by(Purchase.currency):
        currency_summary_table[purchase.currency] += purchase.amount
        # Faust provides semantics for classifying specifically which pool of data is desired from a window, 
        # such as current(), now(), relative_to_now(), etc.
        print(f"{purchase.currency} : {currency_summary_table[purchase.currency].current()}") # try it without current() !


if __name__ == "__main__":
    app.main()
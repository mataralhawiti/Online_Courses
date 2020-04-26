"""
Faust provides an API for creating stateful applications with streaming Tables.

- Faust tables are defined with (app.Table) and take a table name and default type argument.
- Tables must be co-partitioned with the streams they are aggregating. 
- Use the group_by operation to ensure co-partitioning.
- Tables which are not co-partitioned may lead to inaccurate results.

"""


import faust
from dataclasses import dataclass, asdict
import json


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
)


@app.agent(topic)
async def purchase(purchases):
    # must cco-partition (group_by)
    async for purchase in purchases.group_by(Purchase.currency):
        currency_summary_table[purchase.currency] += purchase.amount
        print(f"{purchase.currency} : {currency_summary_table[purchase.currency]}")


if __name__ == "__main__":
    app.main()
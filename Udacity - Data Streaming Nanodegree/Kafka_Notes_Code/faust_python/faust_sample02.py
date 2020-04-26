"""
Deserializing in Faust
"""

import faust
from dataclasses import dataclass, asdict
import json


# Models describe how messages are serialized
# for complex Models, we need to inhert from faust.Record
# this way we can use that model either a key or value.
@dataclass
class Purchase(faust.Record):
    username: str
    currency: str
    amount: int


app = faust.App("2ndFaustApp", broker="localhost:9092")
topic = app.topic(
    "com.udacity.streams.purchases",
    key_type=str,
    value_type=Purchase
)


@app.agent(topic)
async def purchase(purchases):
    async for purchase in purchases:
        print(json.dumps(asdict(purchase), indent=2))


if __name__ == "__main__":
    app.main()
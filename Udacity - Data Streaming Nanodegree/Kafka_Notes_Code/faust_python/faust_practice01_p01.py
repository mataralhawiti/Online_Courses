"""
Producer to generate data to be consumed by ourFaust App 
"""

"""
Retrieving Data from Kafka

Consumer.poll() Vs. Consumer.consume()

"""


from itertools import count
import asyncio
from dataclasses import dataclass, field, asdict
import json
import random
import uuid
from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient, NewTopic
from datetime import datetime, timezone
BROKER_URL = "PLAINTEXT://localhost:9092"
TOPIC_NAME = "withdrawals"

@dataclass
class Withdrawal():
    user: str
    country: str
    amount: float
    date: datetime = None

    def serilize(self):
        return asdict(self)

def generate_withdrawals_dict(n: int = None):
    num_countries = 5
    countries = [f'country_{i}' for i in range(num_countries)]
    country_dist = [0.9] + ([0.10 / num_countries] * (num_countries - 1))

    num_users = 500
    users = [f'user_{i}' for i in range(num_users)]
    for _ in range(n) if n is not None else count():
        yield {
            'user': random.choice(users),
            'amount': random.uniform(0, 25_000),
            'country': random.choices(countries, country_dist)[0],
            'date': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
        }


def generate_withdrawals(n: int = None):
    for d in generate_withdrawals_dict(n):
        yield Withdrawal(**d).serilize()

# for withdrawal in generate_withdrawals(7):
#     print(withdrawal.get("user"))


def create_topic(client):
    """Creates the topic with the given topic name"""
    client = AdminClient({"bootstrap.servers": BROKER_URL})
    futures = client.create_topics(
        [NewTopic(
            topic=TOPIC_NAME, num_partitions=1, replication_factor=1
        )]
    )

    for _, future in futures.items():
        try:
            future.result()
        except Exception as e:
            pass


async def produce(topic_name):
    """Produces data into the Kafka Topic"""
    p = Producer({"bootstrap.servers": BROKER_URL})
    while True:
        for withdrawal in generate_withdrawals(10000):
            p.produce(topic_name, key=withdrawal.get("user"), value=json.dumps(withdrawal))
        await asyncio.sleep(10)


async def produce_consume(topic_name):
    """Runs the Producer and Consumer tasks"""
    t1 = asyncio.create_task(produce(topic_name))
    await t1


def main():
    create_topic(TOPIC_NAME)
    try:
        asyncio.run(produce_consume(TOPIC_NAME))
    except KeyboardInterrupt as e:
        print("shutdwon")


if __name__ == "__main__":
    main()

# ./bin/kafka-console-consumer --bootstrap-server localhost:9092 --topic withdrawals --from-beginning
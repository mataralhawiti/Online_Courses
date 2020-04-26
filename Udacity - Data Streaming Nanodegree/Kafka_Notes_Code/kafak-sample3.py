"""
Sync vs Asycn producer

python3.8 -m pip install confluent-kafka
python3.8 -m pip install faker
"""

from dataclasses import dataclass, field, asdict
import json
import random
from datetime import datetime
import asyncio

from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient, NewTopic
from faker import Faker

faker = Faker()

BROKER_URL = "PLAINTEXT://localhost:9092"
TOPIC_NAME = "org.udacity.exercise3.purchases"


@dataclass
class Purchase:
    username: str = field(default_factory=faker.user_name)
    currency: str = field(default_factory=faker.currency_code)
    amount: int = field(default_factory=lambda: random.randint(100, 200000))


    def serialize(self):
        return json.dumps(asdict(self))

        """
        # or
        return json.dumps(
            {
                "username": self.username,
                "currency": self.currency,
                "amount": self.amount,
            }
        )
        """


def create_topic(client):
    """Creates the topic with the given topic name"""
    client = AdminClient({"bootstrap.servers": BROKER_URL})
    futures = client.create_topics(
        [NewTopic(
            topic=TOPIC_NAME, num_partitions=5, replication_factor=1
            )]
    )

    for _, future in futures.items():
        try:
            future.result()
        except Exception as e:
            pass

async def produce(topic_name):
    """Produces data synchronously into the Kafka Topic"""
    p = Producer({"bootstrap.servers": BROKER_URL})

    start_time = datetime.utcnow()
    curr_iteration = 0 
    while True:
        p.produce(topic_name, Purchase().serialize())
        #p.flush() # this fun will make our producer sync .. tells it stop and send!

        if curr_iteration % 1000 == 0:
            elapsed = (datetime.utcnow() - start_time).seconds
            print(f"messages sent : {curr_iteration} | Total elapsed seconds : {elapsed}")
        curr_iteration += 1


async def produce_consume(topic_name):
    """Runs the Producer and Consumer tasks"""
    t1 = asyncio.create_task(produce(topic_name))
    await t1


def main():
    """check for topic, and create it if not exists"""
    create_topic(TOPIC_NAME)
    try:
        asyncio.run(produce_consume(TOPIC_NAME))
    except KeyboardInterrupt as e:
        print("shutting down")

if __name__ == "__main__":
    main()
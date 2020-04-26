"""
Retrieving Data from Kafka

Consumer.poll() Vs. Consumer.consume()

"""

import asyncio
from dataclasses import dataclass, field, asdict
import json
import random
import uuid

from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient, NewTopic
from faker import Faker

faker = Faker()
BROKER_URL = "PLAINTEXT://localhost:9092"
TOPIC_NAME = "com.udacity.streams.purchases9999"


@dataclass
class Purchase:
    username: str = field(default_factory=faker.user_name)
    currency: str = field(default_factory=faker.currency_code)
    amount: int = field(default_factory=lambda: random.randint(100, 200000))

    # def serialize(self):
    #     return json.dumps(asdict(self))
    def serialize(self):
        return asdict(self)


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
        for _ in range(10):
            tmp = Purchase().serialize()
            p.produce(topic_name, key=tmp.get("username"), value=json.dumps(tmp))
        await asyncio.sleep(10)


# async def produce(topic_name):
#     """Produces data into the Kafka Topic"""
#     p = Producer({"bootstrap.servers": BROKER_URL})

#     curr_iteration = 0
#     while True:
#         p.produce(topic_name, f"iteration {curr_iteration}".encode("utf-8"))
#         curr_iteration += 1
#         await asyncio.sleep(0.1)


# using Consumer.consume()
# Consumer.consume() retunes list() of messages
async def consume(topic_name):
    """Creates the topic with the given topic name"""
    # sleep for few seconds to give Producer time to create data
    await asyncio.sleep(8)

    # Set the offset reset to earliest
    c = Consumer({
        "bootstrap.servers":BROKER_URL,
        "group.id": "0"
    })
    
    # Configure the on_assign callback
    c.subscribe([topic_name])
    
    while True:
        messsages = c.consume(5, timeout=3)
        for messsage in messsages:
            if messsage is None:
                print("no message received by consumer")
            elif messsage.error() is not None:
                print(f"error from consumer {messsage.error()}")
            else:
                print(f"consumed messaged {messsage.key()} : {messsage.value()} ")
        await asyncio.sleep(1)

        # for messsage in messsages:
        #     print(f"consumed messaged {messsage.key()} : {messsage.value()} ")
        # await asyncio.sleep(1)




async def produce_consume(topic_name):
    """Runs the Producer and Consumer tasks"""
    t1 = asyncio.create_task(produce(topic_name))
    t2 = asyncio.create_task(consume(topic_name))
    await t1
    await t2


def main():
    """Checks for topic and creates the topic if it does not exist"""
    client = AdminClient({"bootstrap.servers": BROKER_URL})

    # create topic
    create_topic(client)

    # start the producer and the consumer
    try:
        asyncio.run(produce_consume(TOPIC_NAME))
    except KeyboardInterrupt as e:
        print("shutting down")

if __name__ == "__main__":
    main()

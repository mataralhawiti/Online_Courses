"""
Consumer Offsets
"""

import asyncio

from confluent_kafka import Consumer, Producer, OFFSET_BEGINNING
from confluent_kafka.admin import AdminClient, NewTopic

BROKER_URL = "PLAINTEXT://localhost:9092"
TOPIC_NAME = "com.udacity.lesson2.exercise5.iterations"


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
    """Produces data into the Kafka Topic"""
    p = Producer({"bootstrap.servers": BROKER_URL})

    curr_iteration = 0
    while True:
        p.produce(topic_name, f"iteration {curr_iteration}".encode("utf-8"))
        curr_iteration += 1
        await asyncio.sleep(0.1)


async def consume(topic_name):
    """Creates the topic with the given topic name"""
    # sleep for few seconds to give Producer time to create data
    await asyncio.sleep(2.5)

    # Set the offset reset to earliest
    c = Consumer({
        "bootstrap.servers":BROKER_URL,
        "group.id": "0",
        "auto.offset.reset": "earliest", # to read from the begingin .. First time only
    })
    
    # Configure the on_assign callback
    c.subscribe([topic_name], on_assign=on_assign)
    
    while True:
        messsage = c.poll(1.0)
        if messsage is None:
            print("no message received by consumer")
        elif messsage.error() is not None:
            print(f"error from consumer {messsage.error()}")
        else:
            print(f"consumed messaged {messsage.key()} : {messsage.value()} ")
        await asyncio.sleep(1)

def on_assign(consumer, partitions):
    """Callback for when topic assignment takes place"""
    for partition in partitions:
        partition.offset = OFFSET_BEGINNING

    #Assign the consumer the partitions
    consumer.assign(partitions)

    
async def produce_consume(topic_name):
    """Runs the Producer and Consumer tasks"""
    t1 = asyncio.create_task(produce(topic_name))
    t2 = asyncio.create_task(consume(topic_name))
    await t1
    await t2


def main():
    """" Run """
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


""""
Note 1:
if we run the code as is without "auto.offset.reset": "earliest" config, The Consumer will get messages after we susbcribed.
setting that config will allow our consumer to cosume data from the beginging once it's first subscribed to a topic.

Note 2:
we need to use on_Assign call back 


"""
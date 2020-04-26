from kafka import KafkaConsumer

def consume(topic):
    consumer = KafkaConsumer(
        group_id="police_cosumer01",
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset="earliest"
    )

    consumer.subscribe([topic])

    while True:
        for message in consumer:
            print(message)
    consumer.close()

if __name__ == '__main__':
    consume("policed.epartment.calls02")
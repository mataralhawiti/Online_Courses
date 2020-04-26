from kafka import KafkaProducer
import json
import time


class ProducerServer(KafkaProducer):

    def __init__(self, input_file, topic, **kwargs):
        super().__init__(**kwargs)
        self.input_file = input_file
        self.topic = topic

    def generate_data(self):
        with open(self.input_file, "r") as f:
            data = json.load(f)
            for line in data:
                message = self.dict_to_binary(line)
                self.send(self.topic, message)
                time.sleep(1)

    def dict_to_binary(self, json_dict):
        return json.dumps(json_dict).encode('utf-8')


def run_kafka_server():
    	# TODO get the json file path
    input_file = "/mnt/c/Users/user/udacity_spark/police-department-calls-for-service.json"

    # TODO fill in blanks
    producer = ProducerServer(
        input_file=input_file,
        topic="policed.epartment.calls02",
        bootstrap_servers="localhost:9092",
        client_id="pd01"
    )

    return producer


def feed():
    producer = run_kafka_server()
    producer.generate_data()


if __name__ == "__main__":
    feed()
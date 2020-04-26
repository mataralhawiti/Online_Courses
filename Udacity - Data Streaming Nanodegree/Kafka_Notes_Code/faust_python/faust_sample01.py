import faust

#BROKER_URL = "PLAINTEXT://localhost:9092"

app = faust.App("myFirstFautApp", broker="localhost:9092")
topic = app.topic("com.udacity.streams.purchases")


# Agent decorator defines a "stream processor" that essentially consumes from 
# a Kafka topic and does something for every event it receives.
@app.agent(topic)
async def purchase(purchases):
    async for purchase in purchases:
        print(purchase)


if __name__ == "__main__":
    app.main()

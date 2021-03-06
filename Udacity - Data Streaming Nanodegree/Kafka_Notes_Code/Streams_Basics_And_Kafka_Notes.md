# Introduction to Stream Processing

## Glossary of Key Terms You’ll Learn in this Lesson

- `Stream` : An unbounded sequence of ordered, immutable data
- `Stream Processing` : Continual calculations performed on one or more Streams
- `Immutable Data` : Data that cannot be changed once it has been created  
- `Event` : An immutable fact regarding something that has occurred in our system.
- `Batch` Processing : Scheduled, periodic analysis of one or more groups of related data.
- `Data Store` : A generic place that holds data of some kind, like a message queue or data store
- `Stream Processing Application` : An application which is downstream of one or more data streamsand performs some kind of calculation on incoming data, typically producing one or more outputdata streams
- `Stream Processing Framework` : A set of tools, typically bundled as a library, used to constructa Stream Processing Application
- `Real-time` : In relation to processing, this implies that a piece of data, or an event, is processed almost as soon as it is produced. Strict time-based definitions of real-time are controversial in the industry and vary widely between applications.
For example, a Computer Vision application may consider real-time to be 1 millisecond or less, whereas a data engineering teammay consider it to be 30 seconds or less. In this class when the term "real-time" is used, thetime-frame we have in mind is seconds.
- `Append-only Log` : files in which incoming events are written to the end of the file as they arereceived
- `Change Data Capture (CDC)` : The process of capturing change events, typically in SQL databasesystems, in order to accurately communicate and synchronize changes from primary to replica nodesin a clustered system.
- `Log-Structured Storage` : Systems built on Append-Only Logs, in which system data is stored inlog format.
- `Merge (Log Files)` : When two or more log files are joined together into a single output log file
- `Compact (Log Files)` : When data from one or more files is deleted, typically based on the age ofdata
- `Source (Kafka)` : A term sometimes used to refer to Kafka clients which are producing data intoKafka, 
typically in reference to another data store.
- `Sink (Kafka)` : A term sometimes used to refer to Kafka clients which are extracting data fromKafka, 
typically in reference to another data store.
- `Topic (Kafka)` : A logical construct used to organize and segment datasets within Kafka, similarto how SQL databases use tables.
- `Producer (Kafka`) : An application which is sending data to one or more Kafka Topics.
- `Consumer (Kafka)` : An application which is receiving data from one or more Kafka Topics.


## Event services vs. message services
There's an important distinction to note between services that deliver an event and services that deliver a message.
- Event : 
    - An event is a lightweight notification of a condition or a state change.
        - The publisher of the event has **`no expectation about how the event is handled`**.
        - The consumer of the event **`decides what to do with the notification`**.
        - The producer and consumer are loosely coupled and managed independently.
        - Events can be **`discrete`** units or part of a **`series`**.<br/>
            - **Discrete events** report state change and are actionable (discrete fact).
                - To take the next step, the consumer only needs to know that something happened.
                - The event data has information about what happened but doesn't have the data that triggered the event.
                - For example :
                    -     an event notifies consumers that a file was created. It may have general information about the file, but it doesn't have the file itself.
                - Discrete events are ideal for serverless solutions that need to scale.<br/>
            
            - **Series events** report a condition and are analyzable.
                - The events are in a sequence, or a stream of events, over a period of timet and interrelated.
                - The consumer needs the sequenced series of events to analyze what happened.
                - Telemetry is a common use case, for example, health and load monitoring of a system.
                - Another case is event streaming from IoT devices.
                - ex: log data events <br/><br/>

- Message (command):
    - A message is raw data produced by a service to be consumed or stored elsewhere.
        - The message contains the data that triggered the message pipeline.
        - The publisher of the message has an expectation about how the consumer handles the message.
        - he publisher may also **`expect`** that the receiver(s) of a message report back the outcome of the processing, and will make a path available for those reports to be sent back.
        - The transfer of such messages may be subject to certain deadlines, might have to occur at certain times, and may have to be processed in a certain order
        - A contract exists between the two sides.
        - For example:
             -     the publisher sends a message with the raw data, and expects the consumer to create a file from that data and send a response when the work is done.

        - A command is a high-value message and must be delivered at least once.
        - If a command is lost, the entire business transaction might fail.
        - Also, a command shouldn't be processed more than once. Doing so might cause an erroneous transaction.
        - Commands are often used to manage the workflow of a multistep business transaction.

## Notes

- publish-subscribe model
-  capture, retention, and replay of telemetry and event stream data
- Brokered messaging system. It stores messages in a **`"broker"`** (for example, a queue) until the consuming party is ready to receive the messages.
- Advanced messaging features : FIFO, batching/sessions, transactions, dead-lettering, temporal control, routing and filtering, and duplicate detection
- coupling is very loose
- Asynchronous messaging
- The producer and the consumer can communicate directly or optionally through an intermediary entity (message broker).
- serialization format.
- changelog **

## Understanding Stream Processing

- Stream Processing:
        is the act of performing continual calculations on a potentially endless and constantly evolving source of data.
ream Processing applications perform calculations on Data Streams.
- Data Streams consist of a potentially endless stream of immutable data.
- Immutable data does not change: 
  - once the data has been placed in the data stream it can never be updated.
  - Another data entry can be placed in the stream that supersedes the previous data entry if necessary.
- Data throughput:
  - The data throughput to data streams is highly variable.
  -  Some streams will receive thousands or tens of thousands of records per second, and some will receive one or two records per hour.
- Stream Processing is a critical component in :
  - Finding patterns and meaningful data in disparate log messages in a microservices architecture
  - Tracking user-engagement in real time with streaming website analytics
  - Real-time pricing in ride-sharing applications based on demand and environmental conditions
  - Stock buying/selling based on price, news, and social media sentiment

## Batch Processing

- Runs on a scheduled basis
- May run for a longer period of time and write results to a SQL-like store
- May analyze all historical data at once
- Typically works with mutable data and data stores

## Stream Processing

- Runs at whatever frequency events are generated
- Typically runs quickly, updating in-memory aggregates
- Stream Processing applications may simply emit events themselves, rather than write to an event store
- Typically analyzes trends over a limited period of time due to data volume
- Typically analyzes immutable data and data stores


- Batch and Stream processing are not mutually exclusive. 
- Batch systems can create events to feed into stream processing applications, and similarly, 
- stream processing applications can be part of batch processing analyses.



## Components of a Stream Processing Solution

- Streaming data store
  - May look like a message queue, as is the case with Apache Kafka
  - May look like a SQL store, as is the case with Apache Cassandra
  - Responsible for holding all of the **immutable event database** in the system
  - Provides guarantee that data is stored ordered according to the time it was produced
  - Provides guarantee that data is produced to consumers in the order it was received
  - Provides guarantee that the events it stores are **immutable** and **unchangeable**


-  Processing Application and Framework (Streaming calculation)
    - Stream Processing applications sit downstream of the data store
    - Stream Processing applications ingest real-time event data from one or more data streams
    - Stream Processing applications aggregate, join, and find differences in data from these streams
    - Common Stream Processing Application Frameworks in use today include:
        - Confluent KSQL
        - Kafka Streams
        - Apache Flink
        - Apache Samza
        - Apache Spark Structure Streaming
        - Faust Python Library

## Defintion from Microsfot 

- A streaming platform has three key capabilities:
    1. **`Publish and subscribe`** to streams of records, similar to a message queue or enterprise messaging system.
    2. **`Store streams`** of records in a fault-tolerant durable way.
    3. **`Process streams`** of records as they occur.



## Benefits of Stream Processing

   - More scalable due to distributed nature of storage
   - Provides a useful abstraction that decouples applications from each other
   - Allows one set of data to satisfy many use-cases which may not have been predictable when the dataset was originally created
  
   - Built-in ability to ** replay events ** and observe exactly what occurred, and in what order, 
        provides more opportunities to recover from error states or dig into how a particular result was arrived at


## Examples of stream processing solutions :
- A process that sends a receipt to a customer as soon as it receives a purchase event
- A process that calculates the total page visits in the last 15 minutes
- A process that raises an alert if a certain number of error logs are produced by an application in the last 5 minutes


## Examples of batch processing solution
- A daily process which runs sentiment analysis on customer reviews
- A process which pulls metrics from all microservices every 10 seconds and aggregate these metrics into a centralized view

## scenarios are better suited to a traditional SQL Database?
- Performing a calculation across a full historical representation of a dataset
- Storing mutable data in its most up-to-date form
- Running on-demand exploratory queries from business users
- Not 
    - Updating a calculation as soon as an event occurrs in a system 

## Key concepts to remember about stream processing

   - Stream processing applications consist of a stream data store and a stream processing application framework
   - Stream processing solutions do not operate on a scheduled basis
   - Stream processing solutions provide real-time insights based on event data
   - Stream processing solutions are built around generic data events, allowing for flexibility in data processing and highly scalable applications
   - Batch and stream processing solutions can coexist and feed into each other


## Append-Only Logs

- Data streams are Append-Only Logs
    - data streams use append-only logs to have a guarantee ordering based on the time data was produced.
    - Append-onlu log : a text file in which incoming events are written to the end of the log as the received.
    - Streams are append-only logs.
- Append-Only Logs in SQL Databases
    - SQL DBs use append-only log to communicate and synch changes in a process known as Change Data Capture (CDC)
     to keep synch between primary & secondary
    - in Postgres, know as "write-ahead log" (WAL)
    - write-ahead = the log transaction in SQL Server
    - Each insert, update, and delete that changes state is an event. Many databases use a WAL (write-ahead log) internally to append such events durably and quickly to a filesystem before acknowledging the change to clients, after which time in-memory data structures and other, more permanent files are updated with the current state of the records. That way, if the database crashes after the WAL write completes, the WAL can be used to reconstruct and complete any in-flight transactions, once the database is running again.


## Log-Structure Storage

- built to leavrage the Benefits of stream processing, event-driven architecture, and append-only logs.
- common characteristics :
    - consist of many append-only logs on disk
    - Files periodically Merged, or Joined Together into one file... or 
    - Files periodically compacted, where one or more file is deleted, typically based on age 
    - use many log files, instead of just one, which increases speed and recue I/O bottlenecks
- Examples :
    - Cassandra & HBase
        - use SQL-Like interface
        - use append-only, log-structured streams 
        - popular for Batch workloads
    - Apache Kafka
        - message queue based on log-structured, append-only storage.
        - popular for stream processing
        - it might look similar to popular messages queues like RabiitMQ, but it's based
            on differet storage and scaling mechanism 


## Apache Kafka as a Stream Processing Tool

- Provides an easy-to-use **message queue interface** on top of its **append-only log-structured storage** medium
- Kafka is a **log of events** where traditional message queues are typically used as **job queuees**.
- kafka **stores events**, no actions no jobs<br/><br/>
- In Kafka, **an event describes something that has occurred**, where in traditonal messages or **job queuees** are requests for an action to be performed<br/><br/>
- Kafka is **distributed** by default
- Fault **tolerant** by design, meaning it is hard to lose data if a node is suddenly lost
- Kafka **scales** from 1 to thousands of nodes
- Kafka provides **ordering guarantees for data stored within it**, meaning that the order in which data is received is the order in which data will be produced to consumers.
- Commonly used data store for popular streaming tools like Apache Spark, Flink, and Samza<br/><br/>

- **`event queue (like kafka) vs job or command queue`**<br/><br/>
- The term **`Source`** is sometimes used to refer to Kafka clients which are producing data into Kafka, typically in reference to another data store
- The term **`sink`** is sometimes used to refer to Kafka clients which are extracting data from Kafka,typically in reference to another data store

## Apache Kafka ecosystem
- such as ksql (ksqlDB, Kafka connect)


## Streams vs. Tables (In Streaming context, with Kafka as an example)
- Streams :
    - A stream is a durable, partitioned sequence of **`immutable events`**.
    - When a new event is added a stream, it's appended to the partition that its key belongs to.
    - Streams are useful for **`modeling a historical sequence of activity`**. 
    - For example:
        - you might use a stream to model a series of customer purchases or a sequence of readings from a sensor. Under the hood
        
    - streams are simply stored as **Apache Kafka topics** with an ***enforced schema***.
    - You can create a stream from scratch or declare a stream on top of an existing Kafka topic. In both cases, you can specify a variety of configuration options.<br/><br/>



- Tables :
    - A table is a durable, partitioned collection that **`models change over time`**.
    - **`It's mutable`**.
    - By contrast to streams, which represent a historical sequence of events, tables **`represent what is true as of “now”`**.
    - For example :
        - you might model the locations that someone has lived at as a stream: first Miami, then New York, then London, and so forth.You can use a table to roll up this information and tell you where they live right now.
    - Tables can also be used to materialize a view by incrementally aggregating a stream of events.
    - Tables work by leveraging the keys of each event. Keys are used to denote identity. 
    - If a sequence of events shares a key, the last event for a given key represents the most up-to-date information.
        -  compacted topic :
            - Compaction is a process that periodically deletes all but the newest events for each key (log compaction)
    - You can create a table from scratch or declare a table on top of an existing Apache Kafka topic.
    - In either case, the table is not materialized, which limits its ability to be queried.
    - Only tables that are derived from other collections are materialized.
        - **Materialized Views:**
            - The benefit of a materialized view is that it evaluates a query on the changes only (the delta), instead of evaluating the query on the entire table.
            - When a new event is integrated, the current state of the view evolves into a new state. This transition happens by applying the aggregation function that defines the view with the current state and the new event.
            - When a new event is integrated, the aggregation function that defines the view is applied only on this new event, leading to a new state for the view. In this way, a view is never "fully recomputed" when new events arrive. Instead, the view adjusts incrementally to account for the new information, which means that queries against materialized views are highly efficient.
            - ksqlDB leverages the idea of stream/table duality by storing both components of each table:
                - The current state of a table is stored locally and ephemerally on a specific server by using RocksDB. 
                - The series of changes that are applied to a table is stored durably in a Kafka topic and is replicated across Kafka brokers. 
                - If a ksqlDB server with a materialization of a table fails, a new server rematerializes the table from the Kafka changelog.<br/><br/>


---

# Apache Kafka





# ksqlDB vs. Kafka Streams
- **`ksqlDB`** is the streaming database for Apache Kafka. With ksqlDB, you can write event streaming applications by using a lightweight SQL syntax.

- **`Kafka Streams`** is the Kafka library for writing streaming applications and microservices in Java and Scala.

***`ksqlDB is built on Kafka Streams, a robust stream processing framework that is part of Kafka.`***


# ksqlDB 
- Push and Pull queries
    - Query tables and streams by either continuously subscribing to changing query results as new events occur (push queries).
    - or looking up results at a point in time (pull queries), removing the need to integrate separate systems to serve each.



--



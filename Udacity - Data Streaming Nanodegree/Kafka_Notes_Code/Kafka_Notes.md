
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
- Streaming calculation

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
    - in Postgres, know as "write-ahead" log or Wall 


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

- Provides an easy-to-use message queue interface on top of its append-only log-structured storage medium
- Kafka is a log of events
- In Kafka, an event describes something that has occurred, as opposed to a request for an action to be performed
- Kafka is distributed by default
- Fault tolerant by design, meaning it is hard to lose data if a node is suddenly lost
- Kafka scales from 1 to thousands of nodes
- Kafka provides ordering guarantees for data stored within it, meaning that the order in which data is received is the order in which data will be produced to consumers.
- Commonly used data store for popular streaming tools like Apache Spark, Flink, and Samza

- event queue (like kafka) vs job or command queue
- The term **source** is sometimes used to refer to Kafka clients which are producing data into Kafka, 
    typically in reference to another data store
- The term **sink** is sometimes used to refer to Kafka clients which are extracting data from Kafka, 
        typically in reference to another data store

# Apache Kafka

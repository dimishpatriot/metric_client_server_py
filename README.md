# Training Client & Server

In large projects with a large number of users, it is necessary to carefully monitor all processes taking place in it. Information on processes can be represented by various numerical indicators, for example: the number of requests to your application, the response time of your service to each request, the number of users per day, and others. We will refer to these various numerical indicators as metrics.

There are ready-made solutions for collecting, storing and displaying such metrics, for example Graphite, InfluxDB. In this project, we have developed our own system for collecting and storing metrics based on a client-server architecture.

Project include client, debug server and tests from education on the course "Diving in Python" in the coursera platform (https://www.coursera.org/learn/diving-in-python).

## Requirements
- python version > 3.6 (https://www.python.org/downloads/)
- pytest (https://docs.pytest.org/en/stable/getting-started.html)


## Man
To start full testing just type in the console:

**pytest test_client.py**

You may add necessary pytest keys. For example...

...to see all process in console use the pytest key "-s":

**pytest -s test_client.py**

...to see full pytest report in console use the pytest-key "-v":

**pytest -v test_client.py**

...to start test only for get or put requests add pytest-key "-k" with string "get" or "put":

**pytest -k "get" test_client.py**

## In future

Add the server and server tests. In progress..

# Training Client & Server

In large projects with a large number of users, it is necessary to carefully monitor all processes taking place in it. Information on processes can be represented by various numerical indicators, for example: the number of requests to your application, the response time of your service to each request, the number of users per day, and others. We will refer to these various numerical indicators as metrics.

There are ready-made solutions for collecting, storing and displaying such metrics, for example Graphite, InfluxDB. In this project, we have developed our own system for collecting and storing metrics based on a client-server architecture.

Project include client, debug server (for testing of client), server and tests (test_client & test_server) from education on the course "Diving in Python" in the coursera platform (https://www.coursera.org/learn/diving-in-python).

Client and server programs have been successfully tested and delivered 100/100.

## Requirements
- python version > 3.6 (https://www.python.org/downloads/)
- pytest (https://docs.pytest.org/en/stable/getting-started.html)


## Man
To start full testing just type in the console:

**pytest test_client.py**

**pytest test_server.py**

You may add necessary pytest keys. For example...

...to see all process in console use the pytest key "-s":

**pytest -s test_client.py**

**pytest -s test_server.py**

...to see full pytest report in console use the pytest-key "-v":

**pytest -v test_client.py**

**pytest -v test_server.py**

...to start test only for get or put requests add pytest-key "-k" with string "get" or "put":

**pytest -k "get" test_client.py**

**pytest -k "server_fn" test_server.py** (recommends)

**pytest -k "connection" test_server.py** (you need start terminals before. just run **python server.py**)


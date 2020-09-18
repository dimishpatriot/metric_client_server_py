# Training Client & Server

In large projects with a large number of users, it is necessary to carefully monitor all processes taking place in it. Information on processes can be represented by various numerical indicators, for example: the number of requests to your application, the response time of your service to each request, the number of users per day, and others. We will refer to these various numerical indicators as metrics.

There are ready-made solutions for collecting, storing and displaying such metrics, for example Graphite, InfluxDB. In this project, we have developed our own system for collecting and storing metrics based on a client-server architecture.

Project include client, debug server (for testing of client), server and tests (test_client & test_server) from education on the course "Diving in Python" in the coursera platform (https://www.coursera.org/learn/diving-in-python).

Client and server programs have been successfully tested and delivered 100/100.

## Requirements
- python version > 3.6 (https://www.python.org/downloads/)
- pytest (https://docs.pytest.org/en/stable/getting-started.html)
- pytest-html (https://pypi.org/project/pytest-html/)


## Man
To start server just run:

**python3 server.py**

or import and use Server class in your program.

To use Client import and use Client class in your program.

To start full testing just type in the console:

**pytest test.py**

You may add necessary pytest keys and params. For example, to run only one test class:

**pytest test.py::TestServer** or **pytest test.py::TestClient**

...to see all output in console use the pytest key "-s":

**pytest -s test.py**

...to see full pytest report in console use the pytest-key "-v":

**pytest -v test.py**

...to start test only for get or put requests add pytest-key "-k" with string "get" or "put":

**pytest -k "server_fn" test.py** (recommends)

... to generate report in html-file (need install pytest-html plugin before):

**pytest --html=report_filename.html**

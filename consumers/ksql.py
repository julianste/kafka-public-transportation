"""Configures KSQL to combine station and turnstile data"""
import json
import logging

import requests

import topic_check


logger = logging.getLogger(__name__)


KSQL_URL = "http://ksql:8088"

#
# TODO: Complete the following KSQL statements.
# TODO: For the first statement, create a `turnstile` table from your turnstile topic.
#       Make sure to use 'avro' datatype!
# TODO: For the second statment, create a `turnstile_summary` table by selecting from the
#       `turnstile` table and grouping on station_id.
#       Make sure to cast the COUNT of station id to `count`
#       Make sure to set the value format to JSON

KSQL_STATEMENT = """
CREATE TABLE turnstile (
    station_id INTEGER, station_name VARCHAR, line VARCHAR
) WITH (
    KEY = 'station_id', 
    KAFKA_TOPIC = 'com.udacity.turnstile',
    VALUE_FORMAT = 'AVRO'
);
CREATE TABLE TURNSTILE_SUMMARY WITH (VALUE_FORMAT = 'JSON')
AS SELECT station_id, COUNT(station_id) AS count 
FROM turnstile GROUP BY station_id;
"""


def execute_statement():
    """Executes the KSQL statement against the KSQL API"""
    if topic_check.topic_exists("TURNSTILE_SUMMARY") is True:
        return

    logging.debug("executing ksql statement...")

    json_data = json.dumps(
        {
            "ksql": KSQL_STATEMENT,
            "streamsProperties": {"ksql.streams.auto.offset.reset": "earliest"},
        })
    print(json_data)
    resp = requests.post(
        f"{KSQL_URL}/ksql",
        headers={"Content-Type": "application/vnd.ksql.v1+json"},
        data=json_data,
    )

    # Ensure that a 2XX status code was returned
    resp.raise_for_status()


if __name__ == "__main__":
    execute_statement()

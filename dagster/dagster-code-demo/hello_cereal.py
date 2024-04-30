import requests
import csv
from dagster import job, op, get_dagster_logger

@op
def hello_cereal():
    response = requests.get("https://storage.googleapis.com/bck-123-22/cereal.csv")
    lines = response.text.split("\n")
    cereals = [row for row in csv.DictReader(lines)]
    get_dagster_logger().info(f"Found {len(cereals)} cereals")

@job
def hello_cereal_job():
    hello_cereal()

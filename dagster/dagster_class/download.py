from dagster import job, op, get_dagster_logger
import requests
import csv

@op #declares a dagster operation
def download_cereal():
    response = requests.get("https://storage.googleapis.com/bck-123-22/cereal.csv")
    lines = response.text.split("\n")
    cereals = [row for row in csv.DictReader(lines)]
    get_dagster_logger().info(f"Found {len(cereals)} cereals")

@job
def get_cereals_job():
    download_cereal()

from dagster import job, op, get_dagster_logger
import requests
import csv

@op #declares a dagster operation
def download_cereal():
    response = requests.get("https://storage.googleapis.com/bck-123-22/cereal.csv")
    lines = response.text.split("\n")
    cereals = [row for row in csv.DictReader(lines)]
    get_dagster_logger().info(f"Found {len(cereals)} cereals")
    return cereals

@op
def highest_sugar(cereals):
    sorted_sugar = sorted(cereals, key=lambda cereal: cereal["sugars"])
    highest_sugar = sorted_sugar[-1]['name']
    return highest_sugar
    
@op
def highest_protein(cereals):
    sorted_cereals = list(sorted(cereals, key=lambda cereal: cereal["protein"]))
    return sorted_cereals[-1]['name']

@op 
def get_nutritions(highest_sugar, highest_protein):
    logger = get_dagster_logger()
    logger.info(f'Highest sugar in: {highest_sugar}')
    logger.info(f'Highest protein in: {highest_protein}')

@job
def get_cereals_job():
    cereals = download_cereal()
    get_nutritions(
        highest_sugar=highest_sugar(cereals),
        highest_protein=highest_protein(cereals)
    )

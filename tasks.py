# from src.operations.custom_selenium import CustomSelenium
from robocorp.tasks import task
import logging
from RPA.Robocorp.WorkItems import WorkItems
from src.pipelines.news import apnews_pipeline
from src.operations.news_scraper import APNewsScraper

def list_variables():
    library = WorkItems()
    library.get_input_work_item()

    variables = library.get_work_item_variables()
    for variable, value in variables.items():
        logging.info("%s = %s", variable, value)
        

@task
def news_pipeline_task():
    library = WorkItems()
    library.get_input_work_item()
    variables = library.get_work_item_variables()
    apnews_pipeline(
        interface=APNewsScraper(),
        variables=variables,
    )
    print("Done.")


if __name__ == "__main__":
    news_pipeline_task()
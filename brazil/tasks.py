from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from brazil.services.save_data_states import search_for_empty_data_to_save
from brazil.services.update_data_using_ms_base import (
    pipeline_to_save_data_using_ms_source,
)

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute="*/60")),
    name="search_for_empty_data_to_save",
    ignore_result=True,
)
def task_save_br_data_to_database():
    """
    Celery task to save states data to database.
    """
    search_for_empty_data_to_save()
    logger.info("Turicas API data already searched!")
    pipeline_to_save_data_using_ms_source()
    logger.info("MS data already searched!")


@periodic_task(
    run_every=(crontab(minute="*/1")), name="hello_world", ignore_result=True,
)
def hello_world():
    """
    Hello world
    """
    logger.info("Hello world")
    print("Hello world!")

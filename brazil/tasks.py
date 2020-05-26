from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from brazil.services.save_data_states import search_for_empty_data_to_save
from brazil.services.update_data_using_ms_base import (
    pipeline_to_save_data_using_ms_source,
)

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute="*/180")),
    name="search_for_empty_data_to_save_using_API",
    ignore_result=True,
)
def task_save_br_data_to_database():
    """
    Celery task to save states data to database using API.
    """
    search_for_empty_data_to_save()
    logger.info("Turicas API data searched succesfully!")


@periodic_task(
    run_every=(crontab(minute="*/120")),
    name="search_for_empty_data_to_save_using_MS_source",
    ignore_result=True,
)
def task_save_br_data_to_database_using_ms_source():
    """
    Celery task to save states data to database using MS source.
    """
    pipeline_to_save_data_using_ms_source()
    logger.info("MS data searched succesfully!")

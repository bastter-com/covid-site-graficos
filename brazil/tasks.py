from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from brazil.services.save_data_states import search_for_empty_data_to_save

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute="*/90")),
    name="search_for_empty_data_to_save",
    ignore_result=True,
)
def task_save_br_data_to_database():
    search_for_empty_data_to_save()
    logger.info("Saved BR data to database!")

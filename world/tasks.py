from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from world.services.save_total_world_data import (
    search_for_empty_data_to_save_at_totals_data,
)
from world.services.save_country_daily_data import (
    search_for_empty_data_to_save_at_country_data,
)

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute="*/60")),
    name="search_for_empty_data_to_save_at_database",
    ignore_result=True,
)
def task_save_totals_data_to_database():
    """
    Celery task to save countries data and world total data.
    """
    search_for_empty_data_to_save_at_totals_data()
    search_for_empty_data_to_save_at_country_data()
    logger.info("Saved totals data to database!")
    logger.info("Saved country data to database!")

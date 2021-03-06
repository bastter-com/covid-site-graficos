from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from django.core.management import call_command
from brazil.services.save_data_states import (
    search_for_empty_data_to_save,
    search_for_empty_registers_between_two_dates_or_before_first_case,
    save_previous_city_data_to_database,
)
from brazil.services.update_data_using_ms_base import (
    pipeline_to_save_data_using_ms_source,
)

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute=0, hour="*/2")),
    name="search_for_empty_data_to_save_using_API",
    ignore_result=True,
)
def task_save_br_data_to_database():
    """
    Celery task to save states data to database using API.
    """
    search_for_empty_data_to_save()
    logger.info("Turicas API data searched succesfully!")


# @periodic_task(
#     run_every=(crontab(minute="*/70")),
#     name="search_for_empty_data_to_save_using_MS_source",
#     ignore_result=True,
# )
# def task_save_br_data_to_database_using_ms_source():
#     """
#     Celery task to save states data to database using MS source.
#     """
#     pipeline_to_save_data_using_ms_source()
#     logger.info("MS data searched succesfully!")


@periodic_task(
    run_every=(crontab(minute=0, hour=0)),
    name="copy_last_register_when_no_registers",
    ignore_result=True,
)
def task_fix_empty_registers_copying_last_register():
    """
    Celery task to copy the previous register when no existing register
    in some date.
    """
    search_for_empty_registers_between_two_dates_or_before_first_case()
    logger.info("Date parsed succesfully.")

@periodic_task(
    run_every=(crontab(minute=0, hour=1)),
    name="save_previous_city_data_if_exists",
    ignore_result=True,
)
def task_save_previous_city_data_if_exists():
    """
    Celery task to copy the previous register when no existing register
    in some date.
    """
    save_previous_city_data_to_database()
    logger.info("City data task done succesfully.")


@periodic_task(
    run_every=(crontab(0, 0, day_of_month="2-30/2")),
    name="backup_database",
    ignore_result=True,
)
def task_to_backup_database():
    """
    Celery task to backup database.
    """
    call_command("dbbackup")

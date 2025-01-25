import logging

from config import path_to_logfile

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                    filename=f"{path_to_logfile}",
                    filemode="w",
                    encoding="utf-8")

utils_logger = logging.getLogger("app.utils")
external_api_logger = logging.getLogger("app.external_api")
views_logger = logging.getLogger("app.views")
settings_logger = logging.getLogger("app.settings_loger")
decorators_logger = logging.getLogger("app.decorators_logger")
services_logger = logging.getLogger("app.services_logger")

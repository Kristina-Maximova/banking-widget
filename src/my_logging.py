import logging
import os

path_to_logfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs", "my_logs.log")

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                    filename=f"{path_to_logfile}",
                    filemode="w",
                    encoding="utf-8")


utils_logger = logging.getLogger("app.utils")
external_api_logger = logging.getLogger("app.external_api")
views_logger = logging.getLogger("app.views")
settings_loger = logging.getLogger("app.settings_loger")


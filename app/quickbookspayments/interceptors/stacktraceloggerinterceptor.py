import json
import logging
from datetime import datetime

from pytz import timezone

from app.quickbookspayments.interceptors.interceptorinterface import InterceptorInterface
from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface
from app.quickbookspayments.httpclients.response.responseinterface import ResponseInterface
from app.quickbookspayments.paymentclient import PaymentClient


class StackTraceLoggerInterceptor(InterceptorInterface, logging.Logger):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    NOTICE = 'NOTICE'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'
    EMERGENCY = 'EMERGENCY'
    ALERT = 'ALERT'

    def __init__(self, log_to_file: str, timezone_str: str = 'America/Los_Angeles'):
        super().__init__('StackTraceLogger')
        self.log_file = log_to_file
        self.timezone = timezone_str
        self.setup_logger()

    def setup_logger(self):
        handler = logging.FileHandler(self.log_file)
        formatter = logging.Formatter('%(asctime)s\t[%(levelname)s]\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        self.addHandler(handler)
        self.setLevel(logging.DEBUG)

    def before(self, request: RequestInterface, client: PaymentClient) -> None:
        pass

    def after(self, response: ResponseInterface, client: PaymentClient) -> None:
        pass

    def log(self, level: str, message: str, context: dict = None) -> None:
        if context:
            data = json.dumps(context, ensure_ascii=False)
        else:
            data = ''
        line = self.construct_line(level, message, data)
        self.write_to_file(line)

    def construct_line(self, level: str, message: str, data: str) -> str:
        return f"{self.get_current_time()}\t[{level}]\t{data}\t{message}\n"

    def get_current_time(self) -> str:
        tz = timezone(self.timezone)
        now = datetime.now(tz)
        return now.strftime('%Y-%m-%d %H:%M:%S')

    def write_to_file(self, message: str) -> None:
        try:
            with open(self.log_file, 'a') as fp:
                fp.write(message)
        except Exception as e:
            raise RuntimeError(f"Could not open log file {self.log_file} for writing log. Error: {str(e)}")

    def emergency(self, message: str, context: dict = None) -> None:
        self.log(self.EMERGENCY, message, context)

    def alert(self, message: str, context: dict = None) -> None:
        self.log(self.ALERT, message, context)

    def critical(self, message: str, context: dict = None) -> None:
        self.log(self.CRITICAL, message, context)

    def error(self, message: str, context: dict = None) -> None:
        self.log(self.ERROR, message, context)

    def warning(self, message: str, context: dict = None) -> None:
        self.log(self.WARNING, message, context)

    def notice(self, message: str, context: dict = None) -> None:
        self.log(self.NOTICE, message, context)

    def info(self, message: str, context: dict = None) -> None:
        self.log(self.INFO, message, context)

    def debug(self, message: str, context: dict = None) -> None:
        self.log(self.DEBUG, message, context)

    def intercept(self, request: RequestInterface, response: ResponseInterface, client: PaymentClient) -> None:
        context = {
            'Entity': request.get_request_type(),
            'Url': request.get_url(),
            'Intuit-tid': response.get_intuit_tid(),
            'Request-Id': request.get_request_id()
        }
        self.info(
            f"Sending Request for [{request.get_request_type()}] to [{request.get_url()}] with Request-Id: [{request.get_request_id()}].")

        if response.failed():
            self.error(f"Request failed: [{response.get_body()}].", context)
        else:
            self.info("Request succeeded.", context)

    def config(self, configuration: dict) -> None:
        pass

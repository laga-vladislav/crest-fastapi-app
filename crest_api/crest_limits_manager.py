from functools import wraps
from datetime import timedelta, datetime, timezone


class CRestLimitsManager:
    total_operating = 0

    def __init__(self, ten_minutes_limit: int = 480) -> None:
        self.datetime_format = '%Y-%m-%dT%H:%M:%S%z'
        self.history = []
        self.TEN_MINUTES_LIMIT = ten_minutes_limit

    def __call__(self, func):
        @wraps(func)
        async def func_wrapper(*args, **kwargs):
            self.history = [(timestamp, operating_value) for timestamp, operating_value in self.history if datetime.now(timezone.utc) - timestamp <= timedelta(minutes=10)]

            self.total_operating = sum(
                [operating_value for timestamp, operating_value in self.history])

            while self.total_operating > self.TEN_MINUTES_LIMIT:
                self.history = [(timestamp, operating_value) for timestamp, operating_value in self.history if datetime.now(
                    timezone.utc) - timestamp <= timedelta(minutes=10)]
                self.total_operating = sum(
                    [operating_value for timestamp, operating_value in self.history])

            response = await func(*args, **kwargs)

            start_time = datetime.strptime(
                response['time']['date_start'], self.datetime_format).astimezone(timezone.utc)
            operating_value = response['time']['operating']

            self.history.append((start_time, operating_value))

            self.total_operating = sum(
                [operating_value for timestamp, operating_value in self.history])
            print(self.total_operating)

            return response

        return func_wrapper

from crawler.scheduler import CrawlScheduler


class FakeScheduler:
    def __init__(self):
        self.jobs = []
        self.started = False

    def add_job(self, *args, **kwargs):
        self.jobs.append((args, kwargs))

    def start(self):
        self.started = True


def test_delayed_scheduler_start_starts_underlying_scheduler():
    scheduler = CrawlScheduler(categories=["手机数码"], platforms=["jd"])
    fake = FakeScheduler()
    scheduler.scheduler = fake

    scheduler.start(startup_delay=5)

    assert fake.jobs
    assert fake.started is True

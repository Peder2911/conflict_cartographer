import logging
from datetime import date
from dateutil.relativedelta import relativedelta

from lib.api import Api
from evaluations_api import checks,exceptions

logger = logging.getLogger(__name__)

def fc_union(a,b):
    a["features"] += b["features"]
    return a

class Scheduler(Api):
    def schedule_time_period(self,shift=0):
        r = self.fetch_json("",shift=shift)
        for k in ("start","end"):
            r[k] = date.fromisoformat(r[k])
        return r

    def schedule_start_end(self,shift):
        tp = self.schedule_time_period(shift)
        return tp["start"],tp["end"]

class ApiOnSchedule(Api):
    def __init__(self,scheduler_hostname,*args,**kwargs):
        self.scheduler_api = Scheduler(scheduler_hostname) 
        super().__init__(*args,**kwargs)

class Ged(ApiOnSchedule):
    def year_month_pairs(self,shift):
        start,end = self.scheduler_api.schedule_start_end(shift)
        year_months = [(start.year,start.month)]

        i = start + relativedelta(months=1)
        while i <= end:
            year_months.append((i.year,i.month))
            i = i + relativedelta(months=1)
        return year_months

    def _get_ged(self,country,shift,*args):
        data = {"type":"FeatureCollection","features":[]}
        for year,month in self.year_month_pairs(shift):
            data = fc_union(data,self.fetch_json(country,year,month,*args))
        return data

    def points(self,country,shift=-1):
        return self._get_ged(country,shift,"points")

    def buffered(self,country,shift=-1):
        return self._get_ged(country,shift,"buffered",50000)



class Preds(ApiOnSchedule):
    def fetch_json(self,*args,**kwargs):
        """
        Ensures the user can only see their own preds 
        """
        data = super().fetch_json(*args,**kwargs)
        try:
            assert checks.check_geojson_ownership(data,kwargs["user"])
        except AssertionError as ae:
            msg = f"User {kwargs['user']} tried fetching something they didn't own."
            logger.warning(msg)
            raise exceptions.NotAllowed(msg) from ae

        return data

    def list(self,country,user,shift):
        start,end = self.scheduler_api.schedule_start_end(shift)
        return self.fetch_json(
                "shapes",
                country=country,
                start_date=start,
                end_date=end,
                user=user
                )

    def detail(self,shape_id,user):
        return self.fetch_json("shapes",shape_id,user=user)

class Countries(Api):
    def list(self):
        return self.fetch_json("countries",only_active=True)

    def detail(self,gwno):
        return self.fetch_json("countries",gwno)

class Metrics(ApiOnSchedule):
    def fetch_json(self,*args,**kwargs):
        kwargs = {k:v for k,v in kwargs.items() if v is not None}
        return super().fetch_json(*args,**kwargs) 

    def overall(self,user,shift=None):
        return self.fetch_json(user,shift=shift)

    def available(self,user,shift=None):
        return self.fetch_json(user,"countries",shift=shift)

    def country(self,user,gwno,shift=None):
        return self.fetch_json(user,"countries",gwno,shift=shift)

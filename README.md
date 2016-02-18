# datashaka-python-rh

Simple Python3 client for the [DataShaka API](https://github.com/DataShaka/datashaka-api).

Install requirements via

```bash
pip3 install -r requirements.txt
```

Then initialise

```python
from datashaka import DataShaka

token = 'XXXX-XXXX-XXXX'
groupspace = 'Main'
api = DataShaka(token, groupspace)
```

To retrieve CSV-formatted daily sales figures by country for a set time period

```python
q = api.build_retrieve(time_from="2016-01-01", time_to="2016-01-07", 
    signal="{Sales}", context="[Country]", 
    tractor="crop [Country] ~> sort by time ~> group by day ~> sum")
res = api.retrieve(data=q, format=".csv")
```
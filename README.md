# datashaka-python-rh

Simple Python3 client for the [DataShaka API](https://github.com/DataShaka/datashaka-api).

Install requirements via

```
pip3 install -r requirements.txt
```

Then initialise

```Python
from datashaka import DataShaka

token = 'XXXX-XXXX-XXXX'
groupspace = 'Main'
api = DataShaka(token, groupspace)
```
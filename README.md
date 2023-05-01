# sellit_api

MTTA school project
### Credits to @backbonesk and their project django-project-template which was used as a template for our project
#### https://github.com/backbonesk/django-project-template


## Database basic setup

### Load data from fixtures to DB:
`python manage.py loaddata [fixture ...]`

### Dump data from DB to fixtures:
`python manage.py dumpdata core.<ModelClassName> > apps/core/fixtures/<TableName>.json`

## Usage

### Class-based Views

> To deny checking process in the class-based view, you need to specify, which method you want to mark.
> There are two levels of skipping auth check:
> 1. **EXEMPT_AUTH**: skips user authentication (auth header is no longer needed).
> 2. **EXEMPT_API_KEY**: skips request authentication (signature, api_key).

```python
from apps.api.views.base import SecuredView


class ExampleClassBasedView(SecuredView):
    EXEMPT_AUTH = ['GET']
    EXEMPT_API_KEY = ['GET', 'POST']

    def post(self, request):
        pass

    def get(self, request):
        pass
```



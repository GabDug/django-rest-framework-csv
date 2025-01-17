# djangorestframework-csv-3

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/GabDug/django-rest-framework-csv/master.svg)](https://results.pre-commit.ci/latest/github/GabDug/django-rest-framework-csv/master)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![Ruff](https://img.shields.io/badge/ruff-lint-red)](https://github.com/charliermarsh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Up-to-date CSV Tools for Django REST Framework

This project is a fork [django-rest-framework-csv](https://github.com/mjumbewu/django-rest-framework-csv) by [Mjumbe Wawatu Poe](http://www.twitter.com/mjumbewu) and contributors. Original authors do not endorse this fork.

The goal of this fork is to keep the project up-to-date with the latest versions of Django and Python, but also:

- Use modern Python packaging tools (PEP 517/518, PDM support)
- Provide type hints and use type checking tools (mypy)
- Remove deprecated features

## Installation

``` bash
pip install djangorestframework-csv-3
```

or with [PDM](https://pdm.fming.dev):

``` bash
pdm add djangorestframework-csv-3
```

or with [Poetry](https://python-poetry.org/):

``` bash
poetry add djangorestframework-csv-3
```

## Usage

*views.py*

``` python
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from rest_framework_csv import renderers as r

class MyView (APIView):
    renderer_classes = (r.CSVRenderer, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
    ...
```

Alternatively, to set CSV as a default rendered format, add the
following to the `settings.py` file:

``` python
REST_FRAMEWORK = {
    # specifying the renderers
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_csv.renderers.CSVRenderer',
    ),
}
```

## Ordered Fields

By default, a `CSVRenderer` will output fields in sorted order. To
specify an alternative field ordering, you can override the `header`
attribute. There are two ways to do this:

1. Create a new renderer class and override the `header` attribute
    directly:

    > ``` python
    > class MyUserRenderer (CSVRenderer):
    >     header = ['first', 'last', 'email']
    >
    > @api_view(['GET'])
    > @renderer_classes((MyUserRenderer,))
    > def my_view(request):
    >     users = User.objects.filter(active=True)
    >     content = [{'first': user.first_name,
    >                 'last': user.last_name,
    >                 'email': user.email}
    >                for user in users]
    >     return Response(content)
    > ```

2. Use the `renderer_context` to override the field ordering on the
    fly:

    > ``` python
    > class MyView (APIView):
    >     renderer_classes = [CSVRenderer]
    >
    >     def get_renderer_context(self):
    >         context = super().get_renderer_context()
    >         context['header'] = (
    >             self.request.GET['fields'].split(',')
    >             if 'fields' in self.request.GET else None)
    >         return context
    >
    >     ...
    > ```

## Labeled Fields

Custom labels can be applied to the `CSVRenderer` using the `labels`
dict attribute where each key corresponds to the header and the value
corresponds to the custom label for that header.

1. Create a new renderer class and override the `header` and `labels`
attribute directly:

    > ``` python
    > class MyBazRenderer (CSVRenderer):
    >     header = ['foo.bar']
    >     labels = {
    >         'foo.bar': 'baz'
    >     }
    > ```

## Pagination

Using the renderer with paginated data is also possible with the new
`PaginatedCSVRenderer` class and should be used with views
that paginate data

For more information about using renderers with Django REST Framework,
see the [API Guide](http://django-rest-framework.org/api-guide/renderers/) or the [Tutorial](http://django-rest-framework.org/tutorial/1-serialization/).

## What about other tabular formats?

If you're looking for other formats, check out the following packages:

- [drf-excel](https://github.com/wharton/drf-excel) by @wharton which supports Excel format with advanced customization
- [django-rest-pandas](https://github.com/wq/django-rest-pandas) by @wq, which supports XLS, XLSX, CSV, TXT, SVG and more

## Running the tests

To run the tests against the current environment:

``` bash
./manage.py test
```

### Changelog

> This project was forked starting from release 3.0.0.

## 3.0.0

- Drop support for unsupported versions of Django and Python
  - Django: 3.2, 4.1 and 4.2 are supported
  - Python: 3.8, 3.9, 3.10 and 3.11 are supported
- Removed deprecated `writer_opts` parameter from `CSVRenderer.render(...)`. Pass it in the `context_renderer` or on the class.
- Removed deprecated `headers` property from `CSVRenderer`
- Rendering is now exclusively `UTF-8` encoded
- `CSVRenderer` now uses `io.StringIO` instead of `io.BytesIO`
- Added `get_headers(...)` to `CSVRenderer`, used in `tablize(...)` to ease customization

## 2.1.1

- Add support for byte order markers (BOM) (thanks \@Yaoxin)
- Documentation updates (thanks \@rjemanuele and \@coreyshirk)

## 2.1.0

- CSVs with no data still output header labels (thanks \@travisbloom)
- Include a paginated renderer as part of the app (thanks
    \@masterfloda)
- Generators can be used as data sources for CSVStreamingRenderer
    (thanks \@jrzerr)
- Support for non UTF-8 encoding parsing (thanks \@weasellin)

## 2.0.0

- Make `CSVRenderer.render` return bytes, and
    `CSVParser.parse` expect a byte stream.
- Have data-less renders print header row, if header is explicitly
    supplied
- Drop Django 1.7 tests and add Django 1.10 tests
- have `CSVRenderer.tablize` act as a generator when
    possible (i.e., when a header is explicitly specified).
- Add docs for labels thanks to \@radyz
- Fix header rendering in `CSVStreamingRenderer` thanks to
    \@radialnash
- Improve unicode handling, thanks to \@brandonrobertz

## 1.4.0/1.4.1

- Add support for changing field labels in the `CSVRenderer`, thanks
    to \@soby
- Add support for setting `CSVRenderer` headers, labels, and
    writer_opts as `renderer_context` parameters.
- Renamed `CSVRenderer.headers` to `CSVRenderer.header`; old spelling
    is still available for backwards compatibility, but may be removed
    in the future.

## 1.3.4

- Support streaming CSV rendering, via \@ivancrneto
- Improved test configuration and project metadata, via \@ticosax

## 1.3.2/1.3.3

- Support unicode CSV parsing, and universal newlines, with thanks to
    \@brocksamson

## 1.3.1

- Renderer handles case where data is not a list by wrapping data in a
    list, via pull request from \@dougvk
- Better cross Python version support, via \@paurullan and \@vishen

## 1.3.0

- Support for Python 3, derived from work by \@samdobson

## 1.2.0

- Support consistent ordering of fields in rendered CSV; thanks to
    \@robguttman
- Support specifying particular fields/headers in custom CSV renderer
    by overriding the `headers` attribute.

## 1.1.0

- Support simple CSV parsing; thanks to \@sebastibe

## 1.0.1

- Add the package manifest

## 1.0.0

- Initial release

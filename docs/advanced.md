There are 3 thing you should know about:

* `Page` - `pydantic` model that represents paginated results.
* `Params` - class that represents pagination params passed from user.
* `paginate` - function that is used to paginate your query and data.

## `Page` and `Params`

`fastapi-paginate` by default provides you with 2 implementations of `Page` and `Params`.

### 1. `Page` and `Params` (default)

`Params` constrains:

1. `page` >= 0
2. 0 < `size` <= 100 (default value 50)

Data schema of `PaginationParams`:

```json
{
  "page": 0,
  "size": 50
}
```

Data schema of `Page`:

```json
{
  "items": [
    ...
  ],
  "page": 0,
  "size": 50,
  "total": 100
}
```

Can be imported from `fastapi-paginate`.

All integrations with existing libraries are located in `fastapi_paginate.ext` package.

To see fully working integrations usage, please visit this
[link](https://github.com/nazmulnnb/fastapi_paginate/tree/main/examples).


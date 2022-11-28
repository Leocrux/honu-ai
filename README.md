# Marketplace Challenge

A marketplace for service providers.


## API Reference

### Utils

```http
  GET /populate_mock_data
```

Adds 3 items into default collection used for testing.


### Get Available Providers (task 3)

```http
  GET /get_available_providers
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `skills` | `array[string]` | **[required]** Filter by skills. Returns all providers with **all** of skills |
| `budget` | `int` | **[required]** Filter if any of available periods has `days(period)*cost <= budget` |
| `reviews__lt` | `integer` | **[Optional]** Filter by reviews. Returns all providers with greater or equal than this |


### Crud

#### Get all service providers

```http
  GET /service_provider/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | *[Optional]* Filter by name |
| `skills` | `array[string]` | *[Optional]* Filter by skills. Returns all providers with **any** of skills |
| `cost__gte` | `integer` | *[Optional]* Filter by cost. Returns all providers with cost greater or equal than this |
| `cost__lt` | `integer` | *[Optional]* Filter by cost. Returns all providers with cost lower than this |
| `reviews__lt` | `integer` | *[Optional]* Filter by reviews. Returns all providers with reviews lower than this |


#### Create new service provider

```http
  POST /service_provider
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |

Creates a new service provider based on the request body.
Check swagger docs for schema.

#### Fetch a service provider

```http
  GET /service_provider/{id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id` | `string` | **[required]** |

Fetches the single provider's description based on **id**


#### Update a service provider

```http
  PUT /service_provider/{id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id` | `string` | **[required]** |

Updates service provider with ID **id** based on the request body. 
Check swagger docs for schema.

#### Delete a service provider

```http
  DELETE /service_provider/{id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id` | `string` | **[required]** |

Deletes the service provider with ID **id**







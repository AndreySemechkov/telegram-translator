# Test the API by Creating and Querying items

Substitute your endpoints into these curl commands to test the Create, Read, and Delete operations

## CREATE

```bash
curl --request POST \
  --url https://0xfyi15qci.execute-api.us-east-1.amazonaws.com/dev/item \
  --header 'content-type: application/json' \
  --data '{
    "attribute_1": "Pet",
    "attribute_2": "Rock"
  }'
```

#### Expected Response

204 status

```json
{
  "_id": "c6f03ca0-f792-11e9-9534-260a4b91bfe9",
  "data": {
    "attribute_1": "Pet",
    "attribute_2": "Rock"
  }
}
```

## GET

```bash
curl --request GET \
  --url https://0xfyi15qci.execute-api.us-east-1.amazonaws.com/dev/item/c6f03ca0-f792-11e9-9534-260a4b91bfe9 \
  --header 'content-type: application/json'
```

#### Expected Response

200 status

```json
{
  "_id": "c6f03ca0-f792-11e9-9534-260a4b91bfe9",
  "data": {
    "attribute_1": "Pet",
    "attribute_2": "Rock"
  }
}
```

## LIST

```bash
curl --request GET \
  --url https://0xfyi15qci.execute-api.us-east-1.amazonaws.com/dev/item \
  --header 'content-type: application/json'
```

#### Expected Response

200 status

```json
{
  "response_items": [
    {
      "_id": "c6f03ca0-f792-11e9-9534-260a4b91bfe9",
      "data": {
        "attribute_1": "Pet",
        "attribute_2": "Rock"
      }
    },
    {
      "_id": "717c5f36-f799-11e9-a921-1e0e685be73c",
      "data": {
        "attribute_1": "Pete",
        "attribute_2": "Rock"
      }
    }
  ],
  "filter": null
}
```

Tags: #API #Curl #Testing

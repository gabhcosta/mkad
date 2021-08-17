# MKAD

## Overview
This project performs the calculation of the distance between a geographical coordinate and a polygon on the map.

As an example, data from the Moscow Automobile Ring Road (MKAD) is used, but the user can load any valid polygon and perform the calculations.

## Requirements
* Python less than 3.8 (required)
* <a href= "https://yandex.com/dev/maps/geocoder/"> Yandex Geocoder API </a> (required)
* <a href="https://www.docker.com/"> Docker </a> (not required, but recommended)
* <a href= "https://docs.docker.com/compose/"> Docker Compose </a> (not required, but recommended)
* <a href="https://www.postman.com/downloads/"> Postman </a> or some other for API testing tool

## Running in docker
Open linux bash or git bash:
> $ git clone https://github.com/gabhcosta/mkad.git

> $ cd mkad

Open docker-compose.yml and replace "<\<YOUR YANDEX API KEY>>" with a valid yandex key and save.

> $ docker-compose up --build

## Running native
Open linux bash or git bash:
> $ git clone https://github.com/gabhcosta/mkad.git

> $ cd mkad

> $ pip install -e .

> $ cd mkad

Open app_settings.ini and replace "<\<YOUR YANDEX API KEY>>" in [development] with a valid yandex key and save.

> $ python main.py

## Usage Examples
There are 3 urls in the api. The default host is http://localhost:5000

**/api** : Returns a default message for all http methods.
```
response= {
    "Server Status": "Working!!"
}
```

**/api/mkad** : Only the POST method is available.
```
payload= {
    "country": "country",
    "provinces": ["provinces1", " provinces2"],
    "area":"area",
    "locality":"locality",
    "street": "street",
    "house": "house"
}
```
```
response= {
    "Response Status": "Exact or Inaccurate",
    "Point [lon  lat]": "lon lat to the sent address",
    "Address Found": "Exact address found on Yandex API",
    "Distance": "The distance in km if the location is outside, otherwise 0"
}
```
**/api/generic** : Only the POST method is available.
```
payload= {
    "country": "country",
    "provinces": ["provinces1", " provinces2"],
    "area":"area",
    "locality":"locality",
    "street": "street",
    "house": "house",
    "lonlat_list": ["lon1 lat1", "lon2 lat2", "lon3 lat3", "lon4 lat4", "lon5 lat5"]
}
```
```
response={
    "Response Status": "Exact or Inaccurate",
    "Point [lon  lat]": "lon lat to the sent address",
    "Address Found": "Exact address found on Yandex API",
    "Distance": "The distance in km if the location is outside, otherwise 0"
}
```
## General Comments

In order to expose the Yandex search interface as much as possible, the POST payload was built to match the type of response that comes from the API.

All the fields are not required, but the input validators will ask you to have at least 3 fields filled in. You can pass the full address in one field and fill the others with values that don't matter. For /generic, the lonlat_list field is required and must have 3 points that form a valid polygon.

There are some input validators that do not allow:

* Special characters in the search address. ("!@#$\\%^&*()+?_=<>/")
* Invalid lon and lat values.
* Lon and lat values that do not form a polygon.

All validation methods can be found in **/mkad/helpers/input_checkers.py**

## About the Responses

This code was built with the intention of making the most of the Yandex API. Because of this, there are 2 types of valid responses: "Exact" and "Inaccurate".

## -> Exact
This type of response happens when Yandex returns only 1 location for the request.

On **https:localhost:5000/api/mkad**
```
payload= {
    "country": "dont matter",
    "area": "dont matter",
    "locality":"пл. Победы, 3, Moscow, Rússia, 119590"
}
```
```
response= {
    "Response Status": "Exact",
    "Point [lon  lat]": "37.504834 55.730978",
    "Address Found": "Russia, Moscow, Pobedy Square, 3",
    "Distance": "0.0 km"
}
```
On **https:localhost:5000/api/generic**
```
payload= {
    "country": "Brazil",
    "area":"Santa Catarina",
    "locality":"Florianopolis",
    "lonlat_list": ["-80.40604412766334 12.694830944052345", "-81.63651287766334 -56.5771338389153", "-29.95682537766334 -56.38299200927733", "-32.59354412766334 13.208756628211567"]
}

```

```
{
    "Response Status": "Exact",
    "Point [lon  lat]": "-48.618189 -27.581393",
    "Address Found": "Brazil, Santa Catarina, Florianópolis",
    "Distance": "0.0 km"
}
```

## -> Inaccurate
This type of response happens when Yandex returns more than 1 location (limit 10) for the request.

On **https:localhost:5000/api/mkad**
```
payload= {
    "country": "Russia",
    "area":"Moscow",
    "locality":" dont matter"
    
}
```
```
response= {
    "Response Status": "Inaccurate",
    "0": {
        "Point [lon  lat]": "37.617644 55.755819",
        "Address Found": "Russia, Moscow",
        "Distance": "0.0 km"
    },
    "1": {
        "Point [lon  lat]": "36.515241 56.67366",
        "Address Found": "Russia, Tver Region, Ivan'kovo Reservoir",
        "Distance": "105.22 km"
    },
    "2": {
        "Point [lon  lat]": "38.874756 55.531132",
        "Address Found": "Russia, Moscow Region",
        "Distance": "66.78 km"
    },
    "3": {
        "Point [lon  lat]": "37.04928 55.709454",
        "Address Found": "Russia, Moskva River",
        "Distance": "20.55 km"
    },
    "4": {
        "Point [lon  lat]": "37.239193 55.412917",
        "Address Found": "Russia, Moscow, New Moscow",
        "Distance": "26.7 km"
    },
    "5": {
        "Point [lon  lat]": "37.489859 56.298177",
        "Address Found": "Russia, Moscow Region, Moscow Canal",
        "Distance": "43.45 km"
    },
    "6": {
        "Point [lon  lat]": "34.047955 45.059478",
        "Address Found": "Russia, Republic of Crimea, Moskovskoye Highway",
        "Distance": "1196.38 km"
    },
    "7": {
        "Point [lon  lat]": "46.82472 56.036774",
        "Address Found": "Russia, M-7 Volga",
        "Distance": "561.87 km"
    }
}
```

## Running Tests

In the setup.py directory

> $ pip install -e .

> $ pip install pytest

>$ pytest -v




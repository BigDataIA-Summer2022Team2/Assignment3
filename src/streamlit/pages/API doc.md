# API Guide
- [kaggle dataset](https://www.kaggle.com/datasets/a2015003713/militaryaircraftdetectiondataset)
- military aircraft images with aircraft type and bounding box annotations 

> ***Tips***
> - If you start FastAPI on your own machine, default documentation url will be: `http://127.0.0.1:8000/docs`
> - Also if you are using Linux/Unix system machine, you can use **Curl** to test our APIs.
> - Software like **Postman** is also a good choice to test our APIs

## API 1: infoFilterRequest
### 1.1 Input Value
||filename|width|height|class|xmin|ymin|xmax|ymax|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|Value Type|str|int|int|str|int|int|int|int|
|Description|image file name with max 32 length|image width range 0 ~ num|image height range 0 ~ num|aircraft class|aircraft position - xmin coordinate|aircraft position - ymin coordinate|aircraft position - xmax coordinate|aircraft position - ymax coordinate|
|isOption|True|True|True|True|True|True|True|True|
|Default value|""|0|0|""|0|0|0|0|
|Sample value|03c9ba9a9d35977dee2c6841f948296c|2000|1365|F22|686|1014|1028|1200|


### 1.2 Sample Request URL
```
http://127.0.0.1:8000/api/get/infoFilter/?filename=03c9ba9a9d35977dee2c6841f948296c&width=0&height=0&className=F22&xmin=0&ymin=0&xmax=0&ymax=0
```


```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/get/infoFilter/?filename=03c9ba9a9d35977dee2c6841f948296c&width=0&height=0&className=F22&xmin=0&ymin=0&xmax=0&ymax=0' \
  -H 'accept: application/json'
```

### 1.3 Sample Response
> All return response will be in **Json** format
> outside number key is the index number in the csv file, not the index of images
```json
{
  "9": {
    "filename": "03c9ba9a9d35977dee2c6841f948296c",
    "width": "2000",
    "height": "1365",
    "class": "F22",
    "xmin": "686",
    "ymin": "1014",
    "xmax": "1028",
    "ymax": "1200"
  },
  "10": {
    "filename": "03c9ba9a9d35977dee2c6841f948296c",
    "width": "2000",
    "height": "1365",
    "class": "F22",
    "xmin": "1005",
    "ymin": "440",
    "xmax": "1485",
    "ymax": "588"
  }
}
```
---
## API 2: fileNameandClassFilterRequest

### 2.1 Input Value
||class|filename|
|:-:|:-:|:-:|
|Value Type|str|str|
|Description|aircraft class|image file name with max 32 length|
|isOption|True|False|True|
|Default value|User input required|""|
|Sample value|V22|07baa6df06ca535cfa03b55ec741554d|

### 2.2 Sample Request URL
```markdown
http://127.0.0.1:8000/api/get/fileNameAndClass/?className=v22&filename=07baa6df06ca535cfa03b55ec741554d
```

```markdown
curl -X 'GET' \
  'http://127.0.0.1:8000/api/get/fileNameAndClass/?className=v22&filename=07baa6df06ca535cfa03b55ec741554d' \
  -H 'accept: application/json'
```
### 2.3 Sample Response
```json
{
  "18": {
    "filename": "07baa6df06ca535cfa03b55ec741554d",
    "width": "2048",
    "height": "1536",
    "class": "V22",
    "xmin": "337",
    "ymin": "166",
    "xmax": "1265",
    "ymax": "1340"
  }
}
```
---
## API 3: imgSizeRangeFilterRequest
### 3.1 Input Value
||width|height|
|:-:|:-:|:-:|
|Value Type|int|int|
|Description|image width range 0 ~ num|image height range 0 ~ num|
|isOption|False|False|
|Default value|User input required|User input required|
|Sample value|700|700|
### 3.2 Sample Request URL
```markdown
http://127.0.0.1:8000/api/get/imgSizeRange/?width=550&height=500
```

```markdown
curl -X 'GET' \
  'http://127.0.0.1:8000/api/get/imgSizeRange/?width=550&height=500' \
  -H 'accept: application/json'
```
### 3.3 Sample Response
```json
{
  "69": {
    "filename": "0dc3f3e32533d1909ec496e32a3f916c",
    "width": "512",
    "height": "303",
    "class": "SR71",
    "xmin": "178",
    "ymin": "121",
    "xmax": "331",
    "ymax": "209"
  },
  "186": {
    "filename": "2cf1ec46ef1a6534a784b25ce1d07978",
    "width": "512",
    "height": "341",
    "class": "Su57",
    "xmin": "28",
    "ymin": "162",
    "xmax": "236",
    "ymax": "282"
  },
  "187": {
    "filename": "2cf1ec46ef1a6534a784b25ce1d07978",
    "width": "512",
    "height": "341",
    "class": "Su57",
    "xmin": "115",
    "ymin": "43",
    "xmax": "483",
    "ymax": "172"
  }
}
```
---
## API 4: aircraftPositionRangeFilterRequest
### 4.1 Input Value
||xmin|ymin|xmax|ymax|
|:-:|:-:|:-:|:-:|:-:|
|Value Type|int|int|int|int|
|Description|aircraft position - xmin coordinate|aircraft position - ymin coordinate|aircraft position - xmax coordinate|aircraft position - ymax coordinate|
|isOption|True|True|True|True|
|Default value|0|0|0|0|
|Sample value|300|300|500|500|

### 4.2 Sample Request URL
```markdown
http://127.0.0.1:8000/api/get/aircraftPositionRange/?xmin=300&ymin=300&xmax=500&ymax=500
```

```markdown
curl -X 'GET' \
  'http://127.0.0.1:8000/api/get/aircraftPositionRange/?xmin=300&ymin=300&xmax=500&ymax=500' \
  -H 'accept: application/json'
```

### 4.3 Sample Response
```json
{
  "129": {
    "filename": "1deecbebb637c7cfcb1ed6ef993243c1",
    "width": "1500",
    "height": "969",
    "class": "JAS39",
    "xmin": "327",
    "ymin": "308",
    "xmax": "420",
    "ymax": "374"
  }
}
```
---
## API 5: allInfoRequest
### 5.1 Input Value
- No need user input
- It will directly return all images info
### 5.2 Sample Request URL
```markdown
http://127.0.0.1:8000/api/get/allInfo/
```

```markdown
curl -X 'GET' \
  'http://127.0.0.1:8000/api/get/allInfo/' \
  -H 'accept: application/json'
```
### 5.3 Sample Response
```json
{
  "1": {
    "filename": "00b2add164cb42440a52064e390ea3d2",
    "width": "1280",
    "height": "850",
    "class": "B1",
    "xmin": "322",
    "ymin": "112",
    "xmax": "893",
    "ymax": "618"
  },
  "2": {
    "filename": "00b627cb5578bb036edb01cdcf7b56d9",
    "width": "1300",
    "height": "867",
    "class": "F35",
    "xmin": "607",
    "ymin": "204",
    "xmax": "1202",
    "ymax": "529"
  },
  ...
}
```
---
## API 6: aircraftNumandClassFilterRequest
### 6.1 Input Value
||num|class|
|:-:|:-:|:-:|
|Value Type|int|int|
|Description|number of aircrafts in 1 image|specific aircraft class required|
|isOption|False|True|
|Default value|User input required|""|
|Sample value|3|F22|

### 6.2 Sample Request URL
```markdown
http://127.0.0.1:8000/api/get/aircraftNumandClass/?num=3&className=F22
```

```markdown
curl -X 'GET' \
  'http://127.0.0.1:8000/api/get/aircraftNumandClass/?num=3&className=F22' \
  -H 'accept: application/json''
```
### 6.3 Sample Response
```json
{
  "35": {
    "filename": "0e5c0f6d779768a0380765a04b938f7a",
    "class": "F22",
    "count": 3
  },
  "106": {
    "filename": "2dc47416b142bcd4b709011e80ece4eb",
    "class": "F22",
    "count": 3
  }
}
```
---
## API 7: displayRandomNumImages
### 7.1 Input Value
||num|
|:-:|:-:|
|Value Type|int|
|Description|number of random images|
|isOption|False|
|Default value|User input required|
|Sample value|2|

### 7.2 Sample Request URL
```markdown
http://127.0.0.1:8000/api/get/random/2
```

```markdown
curl -X 'GET' \
  'http://127.0.0.1:8000/api/get/random/2' \
  -H 'accept: application/json'

```
### 7.3 Sample Response
```json
{
  "image NO.1": {
    "230": {
      "filename": "3b8c81155b8c537d88d2275dd4dae803",
      "width": "1870",
      "height": "1227",
      "class": "B2",
      "xmin": "133",
      "ymin": "654",
      "xmax": "507",
      "ymax": "956"
    },
    "231": {
      "filename": "3b8c81155b8c537d88d2275dd4dae803",
      "width": "1870",
      "height": "1227",
      "class": "B2",
      "xmin": "1336",
      "ymin": "383",
      "xmax": "1682",
      "ymax": "674"
    },
    "232": {
      "filename": "3b8c81155b8c537d88d2275dd4dae803",
      "width": "1870",
      "height": "1227",
      "class": "F35",
      "xmin": "987",
      "ymin": "740",
      "xmax": "1227",
      "ymax": "811"
    },
    "233": {
      "filename": "3b8c81155b8c537d88d2275dd4dae803",
      "width": "1870",
      "height": "1227",
      "class": "F35",
      "xmin": "1041",
      "ymin": "286",
      "xmax": "1292",
      "ymax": "356"
    }
  },
  "image NO.2": {
    "234": {
      "filename": "3b9882c439ae0a2592b3ebe044dd44df",
      "width": "1000",
      "height": "714",
      "class": "V22",
      "xmin": "22",
      "ymin": "68",
      "xmax": "953",
      "ymax": "545"
    }
  }
}
```
---
## API 8: displayImageInHTML
### 8.1 Input Value
- No need user input
### 8.2 Sample Request URL
- Pass
### 8.3 Sample Response
- It will return a String format image data which can be display in Base64 format in HTML web page.
---
## API 9: displayImageWithAircraftBlock
### 9.1 Input Value
- No need user input
### 9.2 Sample Request URL
- Pass
### 9.3 Sample Response
- It will return a String format image data(whole image with aircraft position colored block) which can be display in Base64 format in HTML web page.
---
## API 10: displayAircraftOnly
### 10.1 Input Value
- No need user input
### 10.2 Sample Request URL
- Pass
### 10.3 Sample Response
- It will return a String format image data(aircraft only) which can be display in Base64 format in HTML web page.
---
## API 11: displayDataCard
### 11.1 Input Value
- No need user input
### 11.2 Sample Request URL
- Pass
### 11.3 Sample Response
- It will return a HTML format page info
---
## API 12: displayPandasProfiling
### 12.1 Input Value
- No need user input
### 12.2 Sample Request URL
- Pass
### 12.3 Sample Response
- It will return a HTML format page info
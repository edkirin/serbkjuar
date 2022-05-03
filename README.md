# SerbKjuAr

What does it do?
- Read png files from source directory
- Parses file name into machine id
- Read machine external_id from database
- Write external_id as text to the image
- Save image in output directory


## Installation

Clone repository
```
$ git clone https://github.com/edkirin/serbkjuar
```

Change directory
```
$ cd serbkjuar
```

Create virtual environment
```
$ virtualenv env
```

Activate virtual environment
```
$ source env/bin/activate
```

Install libs
```
$ pip install -r requirements.txt
```

Check help
```
$ python serbkjuar.py --help

usage: serbkjuar.py [-h] [--source SOURCE] [--out OUT]

Add machine external ids to images

options:
  -h, --help       show this help message and exit
  --source SOURCE  Source directory containing QR images in PNG format
  --out OUT        Output directory
```

## Configuration

Copy template configuration to your local configuration json file.
```
$ cp config-template.json config.json
```

Edit configuration and change required settings.
```json
{
    "db_host": "localhost",
    "db_port": 5432,
    "db_name": "my-db-name",
    "db_user": "my-db-user",
    "db_password": "my-db-password",
    "font_filename": "DejaVuSans.ttf",
    "text_color": "#000000",
    "text_height": 30,
    "text_y_offset": 7
}
```

### Fonts

Check default available fonts in `fonts` directory. If needed, copy your favorite font to this directory and set it in `config.json`.

## Example

```
(env) eden@sunce:[~/apps/televend/serbkjuar]: python serbkjuar.py --source=/tmp/qr --out=/tmp/qrout
INFO: Reading *.png file list from /tmp/qr
INFO: Processing file 1/10: '/tmp/qr/109.png'
INFO: Writing image: '/tmp/qrout/109.png' with external_id ext-109-12345678
INFO: Processing file 2/10: '/tmp/qr/108.png'
INFO: Writing image: '/tmp/qrout/108.png' with external_id ext-108-12345678
INFO: Processing file 3/10: '/tmp/qr/107.png'
INFO: Writing image: '/tmp/qrout/107.png' with external_id ext-107-12345678
INFO: Processing file 4/10: '/tmp/qr/106.png'
INFO: Writing image: '/tmp/qrout/106.png' with external_id ext-106-12345678
INFO: Processing file 5/10: '/tmp/qr/105.png'
INFO: Writing image: '/tmp/qrout/105.png' with external_id ext-105-12345678
INFO: Processing file 6/10: '/tmp/qr/104.png'
INFO: Writing image: '/tmp/qrout/104.png' with external_id ext-104-12345678
INFO: Processing file 7/10: '/tmp/qr/103.png'
INFO: Writing image: '/tmp/qrout/103.png' with external_id ext-103-12345678
INFO: Processing file 8/10: '/tmp/qr/102.png'
INFO: Writing image: '/tmp/qrout/102.png' with external_id ext-102-12345678
INFO: Processing file 9/10: '/tmp/qr/101.png'
INFO: Writing image: '/tmp/qrout/101.png' with external_id ext-101-12345678
INFO: Processing file 10/10: '/tmp/qr/100.png'
INFO: Writing image: '/tmp/qrout/100.png' with external_id ext-100-12345678
```

### Output image

![Sample output image](assets/example-output-101.png "Sample output image")

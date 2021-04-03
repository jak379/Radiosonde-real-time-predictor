# Radiosonde real-time predictor

Radiosonde real-time predictor is a Python library supposed to predict the landing point of meteorological balloons precisely and in real-time based on data from aprs.fi and Mapbox.

This project is still under development.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the project.

```bash
pip install -r requirements.txt
```

Edit configuration file configuration.json (so you can download elevation map tiles from mapbox and download tracking data from aprs.fi):

```bash
"mapbox_token": "YOUR TOKEN",
"aprsfi_token": "YOUR TOKEN"
```
[Get your Mapbox token here](https://docs.mapbox.com/help/glossary/access-token/)
[Get your aprs.fi token here](https://aprs.fi/page/api)

## Usage

```python
python3 predict <radiosonde number>
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
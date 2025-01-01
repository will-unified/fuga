# FUGA Catalog API

This package contains all the functions necessary for connecting to FUGA's Catalog API. It provides a set of tools to interact with the API and retrieve data related to music catalogs.

## Getting Started

To run files in this package, use the following command:

```zsh
python -m scripts.product_test
```

## Features

- Connect to FUGA's Catalog API
- Retrieve and manage catalog data
- Example scripts for common tasks

## Requirements

- Python 3.x
- Necessary dependencies (listed in `requirements.txt`)

## Installation

1. Clone the repository:
   ```zsh
   git clone https://github.com/will-unified/fuga-api-testing.git
   ```
2. Navigate to the project directory:
   ```zsh
   cd fuga-api-testing
   ```
3. Install the required dependencies:
   ```zsh
   pip install -r requirements.txt
   ```

## Usage

To use the functions provided by this package, import the necessary module classes in your Python scripts and call their methods as needed.

Example:

```python
from fuga.api_client import FUGAClient
from fuga.products import FUGAProduct

# Initialize the client
client = FUGAClient(API_URL, USERNAME, PASSWORD)
client.login()

# Initialize the Product
product = FUGAProduct(client)

# Create the product in FUGA
data = {"name": "New Album", "release_date": "2024-12-31"}
response = product.create(product_data)
print("Created Product:", response)
```

## License

TODO - add a licence if this is ever shared as open source

## Acknowledgments

- FUGA for providing the API

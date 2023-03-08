![plot](bhff-logo.png)
# Google Data Transfer
Automating data transfer and processing between Google Forms and Google Sheets, using Google Cloud APIs.
Currently only supports the "Mentoring Reports Default" transfer configuration, used for mentoring report automatization inside BHFF.
## How to install
1. Create and activate conda environment
```
conda create -n google_data_transfer python=3.10
conda activate google_data_transfer
```
2. Install package
```pip install -e .```
## How to run
```python google_data_transfer/cli.py <form-edit-url> <sheet-edit-url> <sheet-name> [--target-col <target-col>]```  

Contact dev at data@bhfuturesfoundation.org for credentials or questions.

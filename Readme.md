# Printer Monitoring System Readme

The Printer Monitoring System is a Python Django-based application designed specifically for monitoring printers at Sheridan College. It supports Lexmark printers and utilizes various algorithms based on the printer model. This readme file provides essential information on how to set up and use the system effectively.

## Requirements

To run the Printer Monitoring System, ensure that you have the following software installed on your system:

- Python (version 3.6 or higher)
- Django (version 2.2 or higher)
- Lexmark printers at Sheridan College
- `Printers.txt` file with printer details (see the format below)

## Installation

1. Clone the repository from [GitHub Repository URL].
2. Navigate to the project directory using the command line.
3. Install the required Python packages by running the following command:


`pip install -r requirements.txt`


## Configuration

1. Open the `Printers.txt` file in the project directory.
2. Add the printers you want to monitor using the following format:

`hostname$model+address # Comments go here`

Example:
```
{
mi-a300b-prn1$Lexmark XS864+10.64.64.160 # Main printer in Building A, Room 300B
mi-a148g-prn1$Lexmark XM7155 # Backup printer in Building A, Room 148G
mi-a200-prn2$Lexmark XS864 # Printer in Building A, Room 200
}
```

Note: You can add comments to provide additional information or context about the printers. Comments should be preceded by a `#` symbol and can be placed anywhere in the line.

## Usage

1. Start the Django server by running the following command:
python manage.py runserver
2. Open your web browser and navigate to `http://127.0.0.0:8000` to access the Printer Monitoring System interface.
3. The system will automatically retrieve printer details from the `Printers.txt` file and display them on the web interface.
4. Monitor printer statuses, ink levels, and other relevant information from the interface.
5. The system will apply different algorithms based on the printer model to provide accurate monitoring data.

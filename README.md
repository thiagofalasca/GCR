# GCR IPTU Generator App

This application was developed for the City Hall of Governador Celso Ramos to simplify the process of generating IPTU (Property Tax) invoices for taxpayers.
The program is implemented in Python and offers a user-friendly graphical interface to input the property registration number and generate the IPTU invoice as a PDF document.

# Features
* Simple graphical user interface (GUI).
* Input the property registration number to generate the IPTU invoice.
* Generates a PDF invoice based on the provided property registration number.
* Requires a data file with all taxpayer information in a specific layout to function properly.

# Prerequisites
Before running the IPTU Generator App, ensure you have the following:

1. Python: Make sure you have Python installed on your system. The app is compatible with Python 3.7 and above.

# Getting Started

To run the IPTU Generator App, follow these steps:

1. Clone the repository from GitHub:

  ~~~
  git clone https://github.com/your_username/iptu-generator.git
  ~~~
2. Navigate to the project directory:

  ~~~
  cd iptu-generator
  ~~~
3. Prepare the data file:

* The IPTU Generator App requires a data file containing all taxpayer information.
* The data file should follow a specific layout, including details such as taxpayer name, property address, property registration number, etc.
* Place the data file in the project directory/Arquivos with the name Dados.

4. Install the required dependencies:

5. Run the app:

  ~~~
  python IPTUDigital.py
  ~~~

# How to Use

1. Launch the IPTU Generator App by executing python IPTUDigital.py.

2. The GUI window will open, prompting you to enter the property registration number of the taxpayer for whom you want to generate the IPTU invoice.

3. Input the property registration number into the designated field.

4. Click the "Generate IPTU" button to initiate the generation process.

5. The app will use the provided property registration number to search for the taxpayer in the Dados file.

6. If the taxpayer is found in the data file, the app will create a PDF document containing the IPTU invoice for that taxpayer.

7. The generated PDF invoice will be saved in the project directory with the filename pdfFinal.pdf.

# Notes
* The IPTU Generator App relies on the accuracy and completeness of the data file, which is provided by the City Hall of Governador Celso Ramos

# ODSAG
ODSAG (Open Data Semantic Annotation and Graph), a chrome extension that automatically annotates any open dataset and creates graphs (minimal and full graphs) from it. 
This work has been accepted at the EGOV 2022 conference. Use the following link for more details: https://researchportal.unamur.be/en/publications/odsag-enhancing-open-data-discoverability-and-understanding-throu .

## How to install
* Clone the repository
* Run backend (built using django):
	* cd od_annotate_backend
	* python manage.py runserver
* Run chrome extension (add extension to chrome): 
	* Step 1: Open the Chrome extension page and turn on "Developer mode"
	* Step 2: Select "Load Unpacked" (extension) and point it to the extension folder - and you are done!

## Interface
![Screenshots of ODSAG using a COVID Dataset from the Namur portal.](/assets/odsag_process.PNG)
Screenshots of ODSAG using a COVID Dataset from the Namur portal.

## Contact Us
Abiola P. Chokki (abiola-paterne.chokki@unamur.be)
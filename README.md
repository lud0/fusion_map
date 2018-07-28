# Fusion map

Single web page project to try out Google Maps API with the Google Fusion Tables.

A map is shown and whenever a valid location is clicked, it is added to a local database, a Fusion Table and
 below the map, in a list of addresses.
A marker is shown on the map at the location using the Fusion Table layer.
The location is considered valid only if an address can be found using the Google Geocoding service and it
isn't a duplicated address.
Everything can be reset clicking on a "Remove All" link.

## Tech Stack

- Django 2 / Python 3
- Javascript/jQuery
- Google Maps API: Map, Geocoder, FusionTablesLayer

## Setup

Steps needed to get it up and running:

1. create a new **google api service account** for the api dashboard:
<https://console.developers.google.com/apis/credentials/serviceaccountkey> and place the downloaded json file
in the root folder of this project, in a file named `credentials.json`
2. create a new empty fusion table <https://fusiontables.google.com> and note the table id
3. share the fusion table with "Anyone with the link" (to enable reading) as well as with
the newly created service account (to enable writing). For the latter, share it with the email that appears
under the `client_email` key in the `credentials.json` file.
4. edit the `secrets.env` file and set the **GOOGLE_API_KEY** and **GOOGLE_FUSIONTABLE_ID**
5. prepare the env and run the server:
```
virtualenv .ve -p python3
source .ve/bin/activate && source secrets.env
pip install -r requirements.txt
./manage.py migrate
./manage.py runserver
```
6. point your browser to http://localhost:8000/ and play around!


## TODO

- add exception handling
- add internal API testing
- Frontend clearly needs some love :)

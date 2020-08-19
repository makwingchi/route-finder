# Route-finder

## Overview
This project is an extension of [this repo](https://github.com/makwingchi/philly-route-finder).
Based in the City of Philadelphia, this application allows users to type in the origin, destination, and 
departure time. At the backend, the app will compute the safest path based on
the user's inputs. It applies the Dijkstra's Algorithm, with the weight
of each edge being the total number of automobile crashes nearby. 

## Tech Stack
- `Django`
- `Django Rest Framework`
- `Django Rest Framework GIS`
- `Django-cors-headers`
- `React`
- `Redux`
- `Redux-thunk`
- `leaflet`
- `React-leaflet`
- `PostGIS (spatial extension of Postgres)`
- `pgrouting (extension for PostGIS)`
- `Bootstrap`
- `HTML/CSS`

## Preview
![demo1](/01.PNG)

![demo2](/02.PNG)
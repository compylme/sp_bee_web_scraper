# sp_bee_web_scraper
A simple app that grabs the letters of the New York Times gane spelling bee.
This app is designed to be deployed on a Cloud platform like (GCP or AWS) so that it can be run on a schedule

The application is written in python using the following libraries
Selenium, Flask, Pytz

Will add more info on how to run

Commands

# to build docker image
docker build -t :image-name .

# to run docker image
docker run --rm -p 8080:8080 -e PORT=8080 :image-name

# to run docker image interactively
docker run -it --rm -p 8080:8080 -e PORT=8080 fetcher
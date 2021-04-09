# Sentiment analysis for stocks web

Simplified web version of the work presented to the [BI MASTER](https://ica.puc-rio.ai/bi-master) course as a prerequisite for completing the course.

The code for this work can be found at this [repository](https://github.com/DuduKling/stocks-sentiment-analysis).

## Web utilization

This repository is hosted on [Heroku](https://www.heroku.com) and can be accessed through this [link](https://bi-master-sentiment-analysis.herokuapp.com).

> It may take a while for the site to load because of all the initialization and packages installation

## The project

This project was developed in [Python](https://www.python.org), with the website developed in [Flask](https://flask.palletsprojects.com/en/1.1.x/).

Front-end made with [Bootstrap 5](https://getbootstrap.com) and [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) template engine.

Data extraction made with the packages [Tweepy](https://www.tweepy.org) (Twitter API) and [PRAW](https://praw.readthedocs.io/en/latest/) (Reddit API).

Sentiment Analysis were processed with [NLTK](https://www.nltk.org), [TextBlob](https://textblob.readthedocs.io/en/dev/) and [AFINN](https://github.com/fnielsen/afinn) packages.

Graphics rendered with [Plotly](https://plotly.com).

All the packages used in this project can be found at the [Pip File](./Pipfile).

## Build & run

### Install packages

Install pipenv package

```console
> pip install pipenv
```

Start the pipenv shell

```console
> pipenv shell
```

Install all the packages from pipfile

```console
> pipenv install
```

### Start the environment

To start the development server

```console
> flask run
```

> It is necessary to fill in the values ​​of the .env file correctly for the data extraction

## Overview

Backend Of tnbCrow. [Learn More](about.md)

## Project Setup

Follow the steps below to set up the project on your environment. If you run into any problems, feel free to leave a GitHub Issue or reach out to any of our communities above.

Update the pip Version:
```shell
python -m pip install --upgrade pip
```

Install required packages:
```shell
pip install -r requirements.txt
```

Run the application:
```shell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Run the application with Docker:
<br>( You need to have [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/install/) installed )
```shell
docker-compose up # add -d to detach from console
```

Create Super User for admin login:
```shell
python manage.py createsuperuser
```

To check styling:
```shell
flake8 --config=.flake8 config v1
```

## Community
Join the community to stay updated on the most recent developments, project roadmaps, and random discussions about completely unrelated topics.

Discrod: https://discord.gg/F6JeuPtKRf

Twitter: https://twitter.com/tnbcrow

Facebook: https://www.facebook.com/tnbcorw

## Donate

All donations will go to thenewboston to help fund the team to continue to develop the community and create new content.

| Coin | Address |
|-|-|
| ![thenewboston Logo](https://github.com/thenewboston-developers/Website/raw/development/src/assets/images/thenewboston.png) | b6e21072b6ba2eae6f78bc3ade17f6a561fa4582d5494a5120617f2027d38797 |
| ![Bitcoin Logo](https://github.com/thenewboston-developers/Website/raw/development/src/assets/images/bitcoin.png) | 3GZYi3w3BXQfyb868K2phHjrS4i8LooaHh |
| ![Ethereum Logo](https://github.com/thenewboston-developers/Website/raw/development/src/assets/images/ethereum.png) | 0x0E38e2a838F0B20872E5Ff55c82c2EE7509e6d4A |

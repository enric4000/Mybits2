# Mybits2
📝  Hackathon organizer app.

## Expected features

- Email sign up ✉️
- Hackathon registration form 📝
- Check-in interface with QR scanner 📱
- Email verification 📨
- Forgot password 🤔
- Internal user role management: Hacker, Organizer, Volunteer, Sponsor and Admin ☕️
- Django Admin dashboard to manually edit applications and users 👓

## Setup

Needs: Python 3.X, virtualenv, Docker, libpq-dev(needed for psycopg2)

## Script run.sh

This scripts builds all containers automaticaly, installing all the requirements

- run : deploys web container and db container!!!
- db : deploys only db container for db maintenance
- test : deploys both web and db container, and runs tests
- clean : cleans all docker data, containers and networks

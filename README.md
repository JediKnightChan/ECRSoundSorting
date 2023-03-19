# JediKnight's web-site template: Django + Vue.js (CoreUI) + Nginx

This is a website template where backend is handled by [Django Rest framework](https://www.django-rest-framework.org/), 
frontend is written in [Vue.js](https://vuejs.org/index.html) (using [CoreUI](https://github.com/coreui/coreui-vue) 
as a template), [Nginx](https://nginx.org/) provides high-level route management and handles static files. 

[Docker Compose](https://docs.docker.com/compose/) is used for containerization and maintenance of 
[Postgres](https://www.postgresql.org/) database. [Celery](https://docs.celeryq.dev/en/stable/) is used for running 
long and scheduled tasks inside Django and is working along with [Redis](https://redis.io/). 
[Gitlab CI/CD](https://docs.gitlab.com/ee/ci/) allows to automatically deploy new commits to master on the
server (if repo is holden on Gitlab, ofc).

In this template the most valuable thing is the setup of all the things mentioned above.

## Backend

With Django Rest site has an authentication system (based on JWT tokens, also validating 
[Recaptcha V3](https://www.google.com/recaptcha/about/)) and a simple blog api.

- Model
- Serializer
- View Set
- Permission policy with [drf-access-policy](https://github.com/rsinger86/drf-access-policy) (you can specify groups 
of users who have access to each view of a view set)
- Optional filtering with django-filter: 2 "datetime in range" fields, filter blog post by user field

An example celery task is present which is scheduled to run every 3 hours.

## Frontend

CoreUI gives a good looking site landing for dashboard, in my opinion. Vue.js meanwhile seems to be the fastest 
frontend framework to learn out of the 3. Frontend includes pages for login, 404, viewing blog posts.

- Authentication is done via [Vuex Store](https://vuex.vuejs.org/guide/) for global state
- Two useful mixins are present for interacting with "List" and "Retrieve" views of Django Rest. List mixin can handle
on-scroll pagination.

[This favicon generator](https://realfavicongenerator.net/) was used.

## Nginx

Nginx has 2 configs for running in https-only mode and in http mode. Additional security features like 
strict MIME type, XSS protection headers are included.

Easiest way to get SSL certificate:

- Get certificate first time (make sure port 80 is free):
`sudo /usr/bin/docker run -it --rm --name certbot -v "/etc/letsencrypt:/etc/letsencrypt" -v "/var/lib/letsencrypt:/var/lib/letsencrypt"  -p 80:80 certbot/certbot certonly`
- Update it:
`sudo /usr/bin/docker run -it --rm --name certbot -v "/etc/letsencrypt:/etc/letsencrypt" -v "/var/lib/letsencrypt:/var/lib/letsencrypt" -v "/var/www/html/.well-known:/var/www/html/.well-known" certbot/certbot renew --webroot --webroot-path /var/www/html`

## Setup

After **creating .env files** and `sudo docker-compose up --build` or `sudo docker-compose -f docker-compose.dev.yml up --build` 
(for dev and http server) some additional setup is required (executing commands on 'web' container).

1. Migrating database: `sudo docker exec <container_id> python manage.py migrate`
2. Collecting static: `sudo docker exec <container_id> python manage.py collectstatic`
3. Creating superuser: `sudo docker exec -it <container_id> python manage.py createsuperuser`

For the setup of Gitlab Runner for CI/CD see their docs for [installing](https://docs.gitlab.com/runner/install/linux-manually.html)
and [registering](https://docs.gitlab.com/runner/register/index.html) runner. Basically:

1. `export arch=$(dpkg --print-architecture)`
2. `curl -LJO "https://gitlab-runner-downloads.s3.amazonaws.com/latest/deb/gitlab-runner_${arch}.deb"`
3. `sudo dpkg -i gitlab-runner_${arch}.deb`
4. `sudo gitlab-runner register`
5. `sudo gitlab-runner start`

## Tips

- Make sure to check out env-files branch to see env. files examples. Without proper
environmental setup it won't be working (eg, declined login as can't validate Recaptcha).

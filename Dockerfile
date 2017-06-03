FROM python:3.6-onbuild

ENV FLASK_CONFIG=production

CMD python manage.py run_gunicorn

FROM python:3.6-onbuild

ENV FLASK_CONFIG=production

EXPOSE 6001

CMD python manage.py run_gunicorn

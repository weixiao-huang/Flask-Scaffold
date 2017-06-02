FROM python:3.6-onbuild

ENV FLASK_CONFIG=production

EXPOSE 5000

CMD python manage.py run_gunicorn

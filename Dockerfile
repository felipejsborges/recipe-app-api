FROM python:3.10-alpine3.19
# It should be the latest LTS version of the python image with alpine (lightweight) version

LABEL maitainer="felipejsborges"

ENV PYTHONUNBUFFERED 1

ARG UID=101

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /usr/src/app/
WORKDIR /usr/src/app/
EXPOSE 8000

# Create a venv to avoid conflitcs with the image packages (edge case)
# Install the requirements
# Remove the /tmp folder to make the image smaller
# Remove python cache files
# Create a user to avoid running the app as root
# Create the media and static folders
ARG DEV=false
RUN python -m venv /py && \
	/py/bin/pip install --upgrade pip && \
	apk add --update --no-cache postgresql-client jpeg-dev && \
	apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
	/py/bin/pip install -r /tmp/requirements.txt && \
	if [ $DEV = "true" ]; \
		then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
	fi && \
	rm -rf /tmp && \
	apk del .tmp-build-deps && \
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf && \
	adduser \
		--uid $UID \
		--disabled-password \
		--no-create-home \
		django-user && \
	mkdir -p /vol/web/media && \
	mkdir -p /vol/web/static && \
	chown -R django-user:django-user /vol/web && \
	chmod -R 755 /vol/web && \
	chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

VOLUME /vol/web/media
VOLUME /vol/web/static

CMD ["run.sh"]

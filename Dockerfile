FROM python:3.10-alpine3.19
# It should be the latest LTS version of the python image with alpine (lightweight) version

LABEL maitainer="felipejsborges"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# Create a venv to avoid conflitcs with the image packages (edge case)
# Install the requirements
# Remove the /tmp folder to make the image smaller
# Remove python cache files
# Create a user to avoid running the app as root
ARG DEV=false
RUN python -m venv /py && \
	/py/bin/pip install --upgrade pip && \
	apk add --update --no-cache postgresql-client && \
	apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
	/py/bin/pip install -r /tmp/requirements.txt && \
	if [ $DEV = "true" ]; \
		then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
	fi && \
	rm -rf /tmp && \
	apk del .tmp-build-deps && \
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf && \
	adduser \
		--disabled-password \
		--no-create-home \
		django-user

ENV PATH="/py/bin:$PATH"

USER django-user

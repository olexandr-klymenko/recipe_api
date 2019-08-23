FROM python:3.7.3-alpine3.10

WORKDIR /usr/src/recipe_api

COPY ./requirements.txt /usr/src/recipe_api/
RUN pip install -r requirements.txt
COPY . /usr/src/recipe_api

EXPOSE 8000
ENV INVOKE_RUN_SHELL="/bin/sh"
CMD ["inv", "run"]

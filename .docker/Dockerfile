FROM python:3.10.10 as build

WORKDIR /usr/app

# create & use venv
RUN python -m venv /usr/app/venv
ENV PATH "/usr/app/venv/bin:$PATH"

# sent log to terminal
ENV PYTHONUNBUFFERED 1

# install libs
COPY requirements.txt .
RUN pip install -U --force-reinstall -r requirements.txt

FROM python:3.10.10

WORKDIR /usr/app

COPY --from=build /usr/app/venv ./venv
ENV PATH="/usr/app/venv/bin:$PATH"

# copy rest of file
COPY . .

#use unprivileged user
# RUN addgroup --gid 1001 --system app && \
#     adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app
# USER app

RUN cat .env

FROM python

ENV HOME=/home/fast \
    APP_HOME=/home/fast/app

RUN mkdir -p $APP_HOME \
 && groupadd -r fast\
 && useradd -r -g fast fast

WORKDIR $HOME

COPY app app
ADD alembic.ini .

RUN pip install --upgrade pip \
 && pip install -r app/requirements.txt \
 && chown -R fast:fast .

USER fast
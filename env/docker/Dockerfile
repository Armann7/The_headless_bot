# first stage
FROM python:3.9-slim AS builder

RUN useradd -ms /bin/bash appuser
USER appuser

# install dependencies to the local user directory
ENV PATH=/home/appuser/.local:/home/appuser/.local/bin:$PATH
COPY requirements.txt .
RUN python -m pip install --upgrade pip --disable-pip-version-check
RUN pip install --user -r requirements.txt

# second stage
FROM python:3.9-slim
LABEL maintainer="armann7@gmail.com"
ENV MAIN=/theheadless

# Create user and group
RUN groupadd -g 3990 appgroup && useradd -u 3990 --gid appgroup -ms /bin/bash appuser
RUN mkdir $MAIN && chown -R appuser:appgroup $MAIN
USER appuser

# update environment variables
ENV PYTHONPATH=$MAIN:$MAIN/app:$PYTHONPATH
ENV PATH=/home/appuser/.local:/home/appuser/.local/bin:$PATH
ENV TZ=Europe/Moscow

COPY --from=builder --chown=appuser:appgroup /home/appuser/.local /home/appuser/.local
WORKDIR $MAIN
COPY --chown=appuser:appgroup . ./
RUN chmod +x env/*.sh

# make sure you include the -u flag to have our stdout logged
CMD [ "python", "-O", "-m", "app" ]




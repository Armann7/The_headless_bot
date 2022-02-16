#!/bin/sh

# bandit
bandit --configfile $MAIN/env/bandit.yaml -r $MAIN/app
if [ $? -ne 0 ]; then
  echo Bandit checks error
  exit 1
fi

# pytest
pytest $MAIN

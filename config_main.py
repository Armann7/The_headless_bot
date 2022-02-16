import os
import logging


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

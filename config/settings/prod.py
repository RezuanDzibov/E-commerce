from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

dotenv_path = Path(f'{BASE_DIR}/.env.prod')
load_dotenv(dotenv_path=dotenv_path)

from .base import *

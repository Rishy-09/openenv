
from openenv.core.env_server import create_fastapi_app
from ..models import WordGameAction, WordGameObservation
from .environment import WordGameEnvironment

app = create_fastapi_app(WordGameEnvironment, WordGameAction, WordGameObservation)

import pytest

from app.image_poster import ImagePoster
from app import config

poster = None


def setup_module() -> None:
    global poster
    poster = ImagePoster(None, 0, config.GOOGLE_API_KEY, config.GOOGLE_SEARCH_ID)


@pytest.mark.app
def test_object():
    global poster
    assert poster is not None, "Не удалось создать объект ImagePoster"


if __name__ == '__main__':
    pytest.main()

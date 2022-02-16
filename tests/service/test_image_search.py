import pytest
from service.image_search import ImageSearch
from app import config

images = ImageSearch(config.GOOGLE_API_KEY, config.GOOGLE_SEARCH_ID)


@pytest.mark.service
def test_object():
    global images
    assert images is not None, "Не удалось создать объект ImageSearch"


@pytest.mark.service
def test_search():
    global images
    url = images.search("Доброе утро, прикол", count_images=5)
    assert url != "", f"Не удалось найти картинку {url}"


if __name__ == '__main__':
    pytest.main()

import pytest
import asyncio
from app.mouth import Mouth, MouthHTTP


def getMouth() -> Mouth:
    if hasattr(getMouth, 'mouth'):
        getMouth.mouth = MouthHTTP()
    return getMouth.mouth


@pytest.mark.skip(reason="Too long time")
@pytest.mark.app
@pytest.mark.parametrize("test_input",
                         [r"Как тебя зовут?",
                          r"Кто ты такой?",
                          r"Как твое имя?",
                          r"Как твои дела?",
                          r"Чем занимаешься?",
                          r"Снятся ли Андроидам электроовцы?"])
def test_Mouth(test_input):
    mouth = getMouth()
    print(f'I: {test_input}')
    # answer = mouth.answer(test_input)
    answer = asyncio.run(mouth.answer(test_input))
    print(f'Robot: {answer}')
    assert answer != ""


if __name__ == '__main__':
    pytest.main()

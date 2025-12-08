from django.core.exceptions import ValidationError
from urllib.parse import urlparse
import re


class ExternalLinkValidator:
    """
    Валидатор, который проверяет отсутствие сторонних ссылок в тексте,
    за исключением youtube.com
    """
    ALLOWED_DOMAINS = ['youtube.com', 'www.youtube.com']
    URL_REGEX = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    def __call__(self, value):
        urls = re.findall(self.URL_REGEX, value)

        for url in urls:
            domain = urlparse(url).netloc.lower()

            # Проверяем, что домен не в списке разрешенных
            if not any(allowed in domain for allowed in self.ALLOWED_DOMAINS):
                raise ValidationError(
                    f'Ссылки на сторонние ресурсы запрещены. Разрешены только YouTube. Обнаружена ссылка: {url}',
                    code='invalid_link'
                )
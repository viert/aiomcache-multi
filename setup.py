from setuptools import setup, find_packages

setup(
    name="aiomcache-multi",
    version="0.1.0",
    description="a minimal aiomcache wrapper to bring memcached distributed storage capabilities",
    url="https://github.com/viert/aiomcache-multi",
    author="Pavel Vorobyov",
    author_email="aquavitale@yandex.ru",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "aiomcache",
    ],
)

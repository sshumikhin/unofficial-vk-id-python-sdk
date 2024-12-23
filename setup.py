"""Скрипт Setup.py для проекта по упаковке."""

from setuptools import setup, find_packages


setup(
    name='unofficial_vk_id_sdk',
    version='0.2.1',
    packages=find_packages(),
    install_requires=[
        "aiohappyeyeballs==2.4.4",
        "aiohttp==3.11.8",
        "aiosignal==1.3.1",
        "annotated-types==0.7.0",
        "attrs==24.2.0",
        "frozenlist==1.5.0",
        "idna==3.10",
        "multidict==6.1.0",
        "propcache==0.2.1",
        "pydantic==2.10.2",
        "pydantic_core==2.27.1",
        "setuptools==75.6.0",
        "typing_extensions==4.12.2",
        "yarl==1.18.0"]
)

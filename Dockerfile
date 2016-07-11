FROM python:3.5

RUN pip install aiohttp
ADD pt-web.py /pt-web.py

CMD python /pt-web.py

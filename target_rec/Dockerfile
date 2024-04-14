# Image: serenashah/wingbolts-ml

FROM python:3.11

RUN pip install tensorflow==2.15
RUN pip install opencv-python
RUN pip install Flask==3.0
COPY test_distinction.py /test_distinction.py
COPY models /models


CMD ["python", "test_distinction.py"]
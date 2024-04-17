# Image: serenashah/wingbolts-ml

FROM python:3.11

RUN apt-get update && apt-get install -y libgl1 
RUN pip install --default-timeout=100 scikit-learn 
RUN pip install matplotlib
RUN pip install --default-timeout=100 tensorflow==2.15 
RUN pip install opencv-python
RUN pip install Flask==3.0
RUN pip install psutil
COPY test_distinction.py /test_distinction.py
COPY models /models


# CMD ["python", "test_distinction.py"]
# Sweet Scoop Selenium test runner.
# Chrome itself runs in the selenium/standalone-chrome container; this image only runs the Python tests.
FROM python:3.11-slim

WORKDIR /tests

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "unittest", "discover", "-v", "-p", "test_*.py"]

# Sweet Scoop backend — Flask API on port 5000
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first so this layer is cached between code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=5000
EXPOSE 5000

# Single process on purpose: users/carts/orders live in memory,
# so running more than one process (or pod) would split that data.
CMD ["python", "app.py"]

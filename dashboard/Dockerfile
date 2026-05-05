# 1. Gunakan image Python yang ringan
FROM python:3.9-slim

# 2. Update pip (bagus untuk kestabilan)
RUN pip install --upgrade pip

# 3. RUN arahan install library anda di sini
RUN pip install streamlit mysql-connector-python pandas plotly

# 4. Salin kod dashboard anda ke dalam container
COPY . /app
WORKDIR /app

# 5. Jalankan dashboard
CMD ["streamlit", "run", "dashboard.py", "--server.port", "8501"]

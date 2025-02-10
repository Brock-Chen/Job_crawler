FROM python:3.11-slim

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libx11-6 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    xdg-utils \
    # fonts-wqy-zenhei \
    --no-install-recommends

# 安裝 Chrome
RUN wget -q -O chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i chrome.deb || (apt-get update && apt-get install -yf) \
    && rm chrome.deb

# 安裝 ChromeDriver
RUN CHROME_FULL_VERSION=$(google-chrome --version | awk '{print $3}') \
    && CHROME_MAJOR_VERSION=$(echo $CHROME_FULL_VERSION | cut -d '.' -f 1) \
    && echo "Detected Chrome version: $CHROME_FULL_VERSION (Major: $CHROME_MAJOR_VERSION)" \
    && CHROMEDRIVER_VERSION=$(wget -qO- https://googlechromelabs.github.io/chrome-for-testing/latest-patch-versions-per-build.json | grep -Po "\"$CHROME_MAJOR_VERSION\.\d+\.\d+\.\d+\"" | head -1 | tr -d '"') \
    && echo "Using Chromedriver version: $CHROMEDRIVER_VERSION" \
    && wget -q --retry-connrefused --waitretry=1 --read-timeout=20 --timeout=15 -t 3 \
        https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf chromedriver-linux64.zip /tmp/chromedriver-linux64

WORKDIR /app

RUN pip install --no-cache-dir \
    selenium==4.15.2 \
    webdriver-manager==4.0.1 \
    pandas==2.1.4 \
    openpyxl==3.1.2

COPY . .

CMD ["python", "main.py"]
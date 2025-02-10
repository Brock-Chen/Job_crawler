from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")  # 避免共享內存限制
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 禁用機器人偵測

# 減少記憶體佔用
chrome_options.add_argument("--disable-features=Translate,RenderAccessibility")
chrome_options.add_argument("--disable-software-rasterizer")

# 提升效能
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--disable-background-networking")
chrome_options.add_argument("--disable-background-timer-throttling")
chrome_options.add_argument("--disable-backgrounding-occluded-windows")
chrome_options.add_argument("--disable-breakpad")
chrome_options.add_argument("--disable-component-update")
chrome_options.add_argument("--disable-default-apps")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-sync")

# 提升兼容性
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")

# 提升 Docker 內的穩定性
chrome_options.add_argument("--disable-ipc-flooding-protection")
chrome_options.add_argument("--disable-site-isolation-trials")
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--disable-crash-reporter")

# 設置 HTTP headers 語言偏好
chrome_options.add_experimental_option('prefs', {
    'intl.accept_languages': "zh-TW,zh",
    'download.prompt_for_download': False,
})

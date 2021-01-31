import os
import sys

try:
    TUYA_USERNAME = os.environ["TUYA_USERNAME"]
    TUYA_PASSWORD = os.environ["TUYA_PASSWORD"]
except:
    print("TUYA_USERNAME or TUYA_PASSWORD not set")
    sys.exit(1)
try:
    TUYA_API_REGION = os.environ["TUYA_API_REGION"]
    TUYA_COUNTRY_CODE = os.environ["TUYA_COUNTRY_CODE"]
    TUYA_BIZ_TYPE = os.environ["TUYA_BIZ_TYPE"]
except:
    TUYA_API_REGION = "us"
    TUYA_COUNTRY_CODE = "54"
    TUYA_BIZ_TYPE = "smart_life" # Could be tuya, smart_life, jinvoo_smart

try:
    MIDEA_USERNAME = os.environ["MIDEA_USERNAME"]
    MIDEA_PASSWORD = os.environ["MIDEA_PASSWORD"]
except:
    print("MIDEA_USERNAME or MIDEA_PASSWORD not set")
    sys.exit(1)

try:
    MIDEA_API_KEY = os.environ["MIDEA_API_KEY"]
except:
    MIDEA_API_KEY = '3742e9e5842d4ad59c2db887e12449f9'

try:
    TELEGRAM_BOT_KEY = os.environ["TELEGRAM_BOT_KEY"]
except:
    print("TELEGRAM_BOT_KEY not set")
    sys.exit(1)

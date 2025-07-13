# ruby-worker-bot/config.py

# 1. आपकी एडमिन ID
ADMIN_IDS = [6056915535]

# 2. आपकी फाइलें, पैक, और सीरीज
# file_type: 'video', 'document', 'series'
FILE_DATA = {
    # --- सिंगल फाइल्स ---
    "Episode1": {
        "type": "video", 
        "id": "BAACAgUAAxkBAAMXaGpSqvDgq-0fAszJ6iItqfYpI7wAAroTAALdcVBXt_ZT-2d9Lno2BA", 
        "caption": "<b>Episode 1</b>\nQuality: 720pHD"
    },
    "Episode2": {
        "type": "video", 
        "id": "BAACAgUAAxkBAAMKaGpLylL2eBYyfy9tX8wqGoVV12gAAv0VAALdcVBXBhEhvub79Q02BA", 
        "caption": "<b>Episode 2</b>\nQuality: 1080p"
    },
    # आप और भी फाइलें यहाँ जोड़ सकते हैं
}

# 3. डिलीट का समय (सेकंड में)
DELETE_DELAY = 900  # 15 मिनट
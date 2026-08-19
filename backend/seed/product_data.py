"""
AgentCart — Seed Data: Categories and Products.

50+ realistic demo products across 7 categories with INR pricing.
All data is fictional — no copyrighted content.
"""

CATEGORIES = [
    {"name": "Laptops", "slug": "laptops", "description": "Notebooks and ultrabooks for work, gaming, and creative tasks"},
    {"name": "Smartphones", "slug": "smartphones", "description": "Latest smartphones from top brands"},
    {"name": "Headphones", "slug": "headphones", "description": "Over-ear, on-ear, and in-ear headphones and TWS earbuds"},
    {"name": "Monitors", "slug": "monitors", "description": "Displays for productivity, gaming, and creative work"},
    {"name": "Keyboards", "slug": "keyboards", "description": "Mechanical and membrane keyboards"},
    {"name": "Mice", "slug": "mice", "description": "Gaming and productivity mice"},
    {"name": "Smartwatches", "slug": "smartwatches", "description": "Fitness trackers and smartwatches"},
]

# category_slug → list of products
PRODUCTS = {
    "laptops": [
        {
            "name": "ProBook Ultra 14",
            "description": "Ultra-thin 14-inch laptop with stunning OLED display, perfect for professionals. Features fast charging and all-day battery life.",
            "brand": "HP",
            "price": 64999.00,
            "rating": 4.5,
            "warranty": "1 Year Onsite",
            "specifications": {
                "processor": "Intel Core i5-1340P",
                "ram": "16 GB DDR5",
                "storage": "512 GB NVMe SSD",
                "display": "14-inch 2.8K OLED, 90Hz",
                "battery": "56 Wh, up to 10 hours",
                "weight": "1.4 kg",
                "os": "Windows 11 Home",
                "ports": "2x USB-C, 1x USB-A, HDMI, 3.5mm audio"
            },
            "inventory": 25
        },
        {
            "name": "IdeaPad Flex 5",
            "description": "Versatile 2-in-1 convertible laptop with touchscreen and stylus support. Great for students and casual users.",
            "brand": "Lenovo",
            "price": 49999.00,
            "rating": 4.2,
            "warranty": "1 Year Carry-in",
            "specifications": {
                "processor": "AMD Ryzen 5 7530U",
                "ram": "8 GB DDR4",
                "storage": "512 GB SSD",
                "display": "14-inch FHD IPS Touch, 300 nits",
                "battery": "52.5 Wh, up to 9 hours",
                "weight": "1.55 kg",
                "os": "Windows 11 Home",
                "ports": "1x USB-C, 2x USB-A, HDMI, SD card"
            },
            "inventory": 40
        },
        {
            "name": "Swift Go 14 AI",
            "description": "AI-ready ultrabook with dedicated NPU for on-device AI tasks. Brilliant 14-inch 2.8K OLED display.",
            "brand": "Acer",
            "price": 74999.00,
            "rating": 4.6,
            "warranty": "2 Years International",
            "specifications": {
                "processor": "Intel Core Ultra 7 155H",
                "ram": "16 GB LPDDR5x",
                "storage": "1 TB PCIe Gen4 SSD",
                "display": "14-inch 2.8K OLED, 120Hz",
                "battery": "65 Wh, up to 12 hours",
                "weight": "1.3 kg",
                "os": "Windows 11 Home",
                "ports": "2x Thunderbolt 4, 1x USB-A, HDMI 2.1"
            },
            "inventory": 15
        },
        {
            "name": "Aspire 7 Gaming",
            "description": "Entry-level gaming laptop with dedicated GPU. Handles popular games at medium-high settings.",
            "brand": "Acer",
            "price": 56999.00,
            "rating": 4.1,
            "warranty": "1 Year Onsite",
            "specifications": {
                "processor": "Intel Core i5-12450H",
                "ram": "16 GB DDR4",
                "storage": "512 GB SSD",
                "display": "15.6-inch FHD IPS, 144Hz",
                "gpu": "NVIDIA RTX 3050 4GB",
                "battery": "50 Wh, up to 6 hours",
                "weight": "2.1 kg",
                "os": "Windows 11 Home"
            },
            "inventory": 30
        },
        {
            "name": "Vostro 15 3530",
            "description": "Reliable business laptop with long battery life and robust build quality. Carbon-neutral certified.",
            "brand": "Dell",
            "price": 42999.00,
            "rating": 4.0,
            "warranty": "1 Year ProSupport",
            "specifications": {
                "processor": "Intel Core i5-1335U",
                "ram": "8 GB DDR4",
                "storage": "512 GB SSD",
                "display": "15.6-inch FHD Anti-Glare",
                "battery": "54 Wh, up to 8 hours",
                "weight": "1.66 kg",
                "os": "Windows 11 Pro"
            },
            "inventory": 50
        },
        {
            "name": "Zenbook 14 OLED",
            "description": "Premium ultrabook with stunning OLED display, military-grade durability, and ultra-portable design.",
            "brand": "ASUS",
            "price": 79999.00,
            "rating": 4.7,
            "warranty": "2 Years Onsite",
            "specifications": {
                "processor": "Intel Core Ultra 5 125H",
                "ram": "16 GB LPDDR5x",
                "storage": "512 GB PCIe 4.0 SSD",
                "display": "14-inch 2.8K OLED, 120Hz, 100% DCI-P3",
                "battery": "75 Wh, up to 14 hours",
                "weight": "1.28 kg",
                "os": "Windows 11 Home"
            },
            "inventory": 20
        },
        {
            "name": "TUF Gaming A15",
            "description": "Durable gaming laptop with military-grade toughness. High refresh rate display and powerful cooling system.",
            "brand": "ASUS",
            "price": 69999.00,
            "rating": 4.3,
            "warranty": "1 Year Onsite",
            "specifications": {
                "processor": "AMD Ryzen 7 7735HS",
                "ram": "16 GB DDR5",
                "storage": "512 GB NVMe SSD",
                "display": "15.6-inch FHD IPS, 144Hz",
                "gpu": "NVIDIA RTX 4050 6GB",
                "battery": "90 Wh, up to 8 hours",
                "weight": "2.2 kg",
                "os": "Windows 11 Home"
            },
            "inventory": 18
        },
        {
            "name": "MacBook Air M3",
            "description": "Ultra-thin and silent laptop with Apple M3 chip. Fanless design, all-day battery, and stunning Liquid Retina display.",
            "brand": "Apple",
            "price": 114900.00,
            "rating": 4.8,
            "warranty": "1 Year Apple Limited",
            "specifications": {
                "processor": "Apple M3 (8-core CPU, 10-core GPU)",
                "ram": "8 GB Unified Memory",
                "storage": "256 GB SSD",
                "display": "13.6-inch Liquid Retina, 500 nits",
                "battery": "52.6 Wh, up to 18 hours",
                "weight": "1.24 kg",
                "os": "macOS Sonoma"
            },
            "inventory": 12
        },
    ],
    "smartphones": [
        {
            "name": "Galaxy S24 FE",
            "description": "Fan edition flagship with Galaxy AI features, bright AMOLED display, and versatile camera system.",
            "brand": "Samsung",
            "price": 49999.00,
            "rating": 4.4,
            "warranty": "1 Year Manufacturer",
            "specifications": {
                "processor": "Samsung Exynos 2400e",
                "ram": "8 GB",
                "storage": "128 GB",
                "display": "6.7-inch Dynamic AMOLED 2X, 120Hz",
                "camera": "50MP + 12MP + 8MP, 10MP front",
                "battery": "4700 mAh, 25W fast charge",
                "os": "Android 14, One UI 6.1",
                "connectivity": "5G, Wi-Fi 6E, NFC"
            },
            "inventory": 35
        },
        {
            "name": "Pixel 8a",
            "description": "Google's AI-first smartphone with exceptional camera and 7 years of updates. Best-in-class photo processing.",
            "brand": "Google",
            "price": 42999.00,
            "rating": 4.5,
            "warranty": "1 Year Manufacturer",
            "specifications": {
                "processor": "Google Tensor G3",
                "ram": "8 GB",
                "storage": "128 GB",
                "display": "6.1-inch OLED, 120Hz",
                "camera": "64MP + 13MP, 13MP front",
                "battery": "4492 mAh, 18W charging",
                "os": "Android 14 (7 years updates)",
                "connectivity": "5G, Wi-Fi 6E, NFC"
            },
            "inventory": 28
        },
        {
            "name": "OnePlus 12R",
            "description": "Performance flagship with Snapdragon 8 Gen 2 and blazing-fast 100W SUPERVOOC charging.",
            "brand": "OnePlus",
            "price": 39999.00,
            "rating": 4.3,
            "warranty": "1 Year Manufacturer",
            "specifications": {
                "processor": "Qualcomm Snapdragon 8 Gen 2",
                "ram": "8 GB LPDDR5X",
                "storage": "128 GB UFS 3.1",
                "display": "6.78-inch LTPO AMOLED, 120Hz",
                "camera": "50MP + 8MP + 2MP, 16MP front",
                "battery": "5500 mAh, 100W SUPERVOOC",
                "os": "Android 14, OxygenOS 14",
                "connectivity": "5G, Wi-Fi 7, Bluetooth 5.3"
            },
            "inventory": 45
        },
        {
            "name": "iPhone 15",
            "description": "Dynamic Island, 48MP camera system, USB-C, and the powerful A16 Bionic chip in a ceramic shield design.",
            "brand": "Apple",
            "price": 69900.00,
            "rating": 4.6,
            "warranty": "1 Year Apple Limited",
            "specifications": {
                "processor": "Apple A16 Bionic",
                "ram": "6 GB",
                "storage": "128 GB",
                "display": "6.1-inch Super Retina XDR, Dynamic Island",
                "camera": "48MP + 12MP, 12MP TrueDepth front",
                "battery": "3349 mAh, 20W wired, 15W MagSafe",
                "os": "iOS 17",
                "connectivity": "5G, Wi-Fi 6, NFC, USB-C"
            },
            "inventory": 22
        },
        {
            "name": "Redmi Note 13 Pro+",
            "description": "Feature-packed mid-range phone with 200MP camera and 120W HyperCharge. Incredible value for money.",
            "brand": "Xiaomi",
            "price": 29999.00,
            "rating": 4.2,
            "warranty": "1 Year Manufacturer",
            "specifications": {
                "processor": "MediaTek Dimensity 7200 Ultra",
                "ram": "8 GB LPDDR4X",
                "storage": "256 GB UFS 2.2",
                "display": "6.67-inch 1.5K AMOLED, 120Hz, 1800 nits",
                "camera": "200MP + 8MP + 2MP, 16MP front",
                "battery": "5000 mAh, 120W HyperCharge",
                "os": "Android 14, MIUI 15"
            },
            "inventory": 60
        },
        {
            "name": "Vivo V30 Pro",
            "description": "Camera-focused smartphone with ZEISS optics and Aura Light portrait system. Stunning night photography.",
            "brand": "Vivo",
            "price": 36999.00,
            "rating": 4.1,
            "warranty": "1 Year Manufacturer",
            "specifications": {
                "processor": "MediaTek Dimensity 8200",
                "ram": "8 GB",
                "storage": "256 GB",
                "display": "6.78-inch 1.5K AMOLED, 120Hz",
                "camera": "50MP ZEISS + 50MP, 50MP front",
                "battery": "5000 mAh, 80W FlashCharge",
                "os": "Android 14, Funtouch OS 14"
            },
            "inventory": 32
        },
        {
            "name": "Nothing Phone (2a)",
            "description": "Unique transparent design with Glyph Interface. Clean software experience with solid mid-range performance.",
            "brand": "Nothing",
            "price": 23999.00,
            "rating": 4.3,
            "warranty": "1 Year Manufacturer",
            "specifications": {
                "processor": "MediaTek Dimensity 7200 Pro",
                "ram": "8 GB",
                "storage": "128 GB",
                "display": "6.7-inch AMOLED, 120Hz, 1300 nits",
                "camera": "50MP + 50MP, 32MP front",
                "battery": "5000 mAh, 45W charging",
                "os": "Android 14, Nothing OS 2.5"
            },
            "inventory": 38
        },
    ],
    "headphones": [
        {
            "name": "WH-1000XM5",
            "description": "Industry-leading noise cancelling headphones with exceptional sound quality and 30-hour battery life.",
            "brand": "Sony",
            "price": 26990.00,
            "rating": 4.8,
            "warranty": "1 Year Manufacturer",
            "specifications": {
                "type": "Over-ear, Wireless",
                "driver": "30mm",
                "anc": "Active Noise Cancelling (Auto NC Optimizer)",
                "battery": "30 hours (NC on), 40 hours (NC off)",
                "charging": "USB-C, 3 min charge = 3 hours playback",
                "codec": "LDAC, AAC, SBC",
                "weight": "250g",
                "features": "Multipoint, Speak-to-Chat, DSEE Extreme"
            },
            "inventory": 30
        },
        {
            "name": "QuietComfort Ultra",
            "description": "Premium ANC headphones with Immersive Audio and CustomTune technology for personalized sound.",
            "brand": "Bose",
            "price": 29990.00,
            "rating": 4.7,
            "warranty": "1 Year Manufacturer",
            "specifications": {
                "type": "Over-ear, Wireless",
                "anc": "Active Noise Cancelling with Aware Mode",
                "battery": "24 hours",
                "charging": "USB-C, 15 min charge = 2.5 hours",
                "codec": "aptX Adaptive, AAC, SBC",
                "weight": "250g",
                "features": "Immersive Audio, CustomTune, Multipoint"
            },
            "inventory": 22
        },
        {
            "name": "Buds Pro 3",
            "description": "True wireless earbuds with Hi-Res audio and AI-enhanced noise cancelling. Compact charging case.",
            "brand": "OnePlus",
            "price": 11999.00,
            "rating": 4.4,
            "warranty": "1 Year Manufacturer",
            "specifications": {
                "type": "TWS In-ear",
                "driver": "11mm + 6mm Dual",
                "anc": "Adaptive ANC up to 49dB",
                "battery": "6 hours (buds), 43 hours (with case)",
                "charging": "USB-C, Wireless",
                "codec": "LHDC 5.0, LDAC, AAC",
                "weight": "5.1g per bud",
                "ip_rating": "IP55"
            },
            "inventory": 55
        },
        {
            "name": "Galaxy Buds FE",
            "description": "Affordable true wireless earbuds with Samsung ANC. Ergonomic wing-tip design for secure fit.",
            "brand": "Samsung",
            "price": 4999.00,
            "rating": 4.1,
            "warranty": "1 Year Manufacturer",
            "specifications": {
                "type": "TWS In-ear",
                "driver": "6.5mm + 5.6mm",
                "anc": "Active Noise Cancelling",
                "battery": "6 hours (buds), 21 hours (with case)",
                "charging": "USB-C",
                "codec": "AAC, SBC, Samsung Scalable Codec",
                "weight": "5.6g per bud",
                "ip_rating": "IPX2"
            },
            "inventory": 70
        },
        {
            "name": "AirPods Pro (2nd Gen)",
            "description": "Active noise cancellation with Adaptive Transparency. Personalized Spatial Audio with dynamic head tracking.",
            "brand": "Apple",
            "price": 24900.00,
            "rating": 4.7,
            "warranty": "1 Year Apple Limited",
            "specifications": {
                "type": "TWS In-ear",
                "chip": "Apple H2",
                "anc": "Active Noise Cancellation + Adaptive Transparency",
                "battery": "6 hours (buds), 30 hours (MagSafe case)",
                "charging": "USB-C, MagSafe, Qi",
                "codec": "AAC",
                "weight": "5.3g per bud",
                "ip_rating": "IP54"
            },
            "inventory": 18
        },
        {
            "name": "Rockerz 450 Pro",
            "description": "Budget wireless headphones with thumping bass and 70-hour battery life. Lightweight and comfortable.",
            "brand": "boAt",
            "price": 1499.00,
            "rating": 3.9,
            "warranty": "1 Year Manufacturer",
            "specifications": {
                "type": "Over-ear, Wireless",
                "driver": "40mm",
                "battery": "70 hours",
                "charging": "USB-C",
                "codec": "SBC",
                "weight": "185g",
                "features": "Dual Equalizer Modes, Foldable"
            },
            "inventory": 100
        },
        {
            "name": "FreeBuds 5i",
            "description": "Well-balanced TWS earbuds with Hi-Res Audio certification and solid noise cancellation at a great price.",
            "brand": "Huawei",
            "price": 5999.00,
            "rating": 4.2,
            "warranty": "1 Year Manufacturer",
            "specifications": {
                "type": "TWS In-ear",
                "driver": "10mm Dynamic",
                "anc": "Hybrid ANC up to 42dB",
                "battery": "7.5 hours (buds), 28 hours (with case)",
                "charging": "USB-C",
                "codec": "LDAC, AAC, SBC",
                "weight": "4.9g per bud",
                "ip_rating": "IP54"
            },
            "inventory": 42
        },
    ],
    "monitors": [
        {
            "name": "UltraSharp U2723QE",
            "description": "27-inch 4K USB-C hub monitor with IPS Black technology. Factory-calibrated for accurate colors.",
            "brand": "Dell",
            "price": 44999.00,
            "rating": 4.6,
            "warranty": "3 Years Premium Panel Exchange",
            "specifications": {
                "size": "27 inches",
                "resolution": "3840 x 2160 (4K UHD)",
                "panel": "IPS Black",
                "refresh_rate": "60Hz",
                "color_accuracy": "98% DCI-P3, Delta E < 2",
                "ports": "USB-C 90W PD, HDMI, DP, USB hub",
                "hdr": "HDR 400",
                "adjustments": "Height, Tilt, Swivel, Pivot"
            },
            "inventory": 15
        },
        {
            "name": "ROG Swift PG27AQN",
            "description": "27-inch 1440p gaming monitor with blazing 360Hz refresh rate. Ultimate competitive gaming display.",
            "brand": "ASUS",
            "price": 89999.00,
            "rating": 4.8,
            "warranty": "3 Years",
            "specifications": {
                "size": "27 inches",
                "resolution": "2560 x 1440 (QHD)",
                "panel": "IPS",
                "refresh_rate": "360Hz",
                "response_time": "1ms GTG",
                "gsync": "NVIDIA G-SYNC",
                "hdr": "HDR 600",
                "ports": "HDMI 2.0, DP 1.4, USB hub"
            },
            "inventory": 8
        },
        {
            "name": "27GP850-B",
            "description": "27-inch QHD Nano IPS gaming monitor with 180Hz refresh and wide color gamut. Great all-rounder.",
            "brand": "LG",
            "price": 29999.00,
            "rating": 4.5,
            "warranty": "3 Years",
            "specifications": {
                "size": "27 inches",
                "resolution": "2560 x 1440 (QHD)",
                "panel": "Nano IPS",
                "refresh_rate": "180Hz (OC)",
                "response_time": "1ms GTG",
                "gsync": "G-SYNC Compatible, FreeSync Premium",
                "color": "98% DCI-P3",
                "ports": "HDMI 2.0, DP 1.4, USB 3.0"
            },
            "inventory": 20
        },
        {
            "name": "Odyssey G5 32",
            "description": "32-inch curved QHD gaming monitor with 165Hz refresh. Immersive 1000R curvature.",
            "brand": "Samsung",
            "price": 24999.00,
            "rating": 4.3,
            "warranty": "3 Years",
            "specifications": {
                "size": "32 inches",
                "resolution": "2560 x 1440 (QHD)",
                "panel": "VA, 1000R Curved",
                "refresh_rate": "165Hz",
                "response_time": "1ms MPRT",
                "gsync": "FreeSync Premium",
                "hdr": "HDR10",
                "ports": "HDMI 2.0, DP 1.2"
            },
            "inventory": 25
        },
        {
            "name": "ProDisplay 24",
            "description": "Affordable 24-inch FHD IPS monitor for everyday work. Eye comfort with flicker-free and low blue light.",
            "brand": "HP",
            "price": 11999.00,
            "rating": 4.0,
            "warranty": "3 Years",
            "specifications": {
                "size": "23.8 inches",
                "resolution": "1920 x 1080 (FHD)",
                "panel": "IPS",
                "refresh_rate": "75Hz",
                "response_time": "5ms GTG",
                "color": "99% sRGB",
                "ports": "HDMI, VGA",
                "features": "Eye Ease, Anti-glare"
            },
            "inventory": 40
        },
    ],
    "keyboards": [
        {
            "name": "MX Keys S",
            "description": "Premium wireless keyboard with smart backlit keys that adjust to lighting. Perfect Flow cross-computer control.",
            "brand": "Logitech",
            "price": 10995.00,
            "rating": 4.6,
            "warranty": "2 Years",
            "specifications": {
                "type": "Membrane (scissor)",
                "connectivity": "Bluetooth, USB receiver (Logi Bolt)",
                "backlight": "Smart Backlight",
                "battery": "Rechargeable, 10 days (backlit), 5 months (no backlight)",
                "layout": "Full-size with numpad",
                "compatibility": "Windows, macOS, Linux, iOS, Android",
                "features": "Easy-Switch (3 devices), USB-C charging"
            },
            "inventory": 30
        },
        {
            "name": "G Pro X TKL",
            "description": "Tournament-grade tenkeyless mechanical gaming keyboard with hot-swappable switches and LIGHTSPEED wireless.",
            "brand": "Logitech",
            "price": 14995.00,
            "rating": 4.5,
            "warranty": "2 Years",
            "specifications": {
                "type": "Mechanical (GX Brown Tactile)",
                "connectivity": "LIGHTSPEED Wireless, Bluetooth, USB-C",
                "backlight": "LIGHTSYNC RGB per-key",
                "battery": "Rechargeable, 50+ hours",
                "layout": "TKL (Tenkeyless)",
                "hot_swappable": "Yes (3-pin/5-pin)",
                "features": "Game Mode, onboard memory"
            },
            "inventory": 20
        },
        {
            "name": "Keychron K8 Pro",
            "description": "Compact TKL mechanical keyboard with QMK/VIA support for full key remapping. Hot-swappable Gateron switches.",
            "brand": "Keychron",
            "price": 8999.00,
            "rating": 4.4,
            "warranty": "1 Year",
            "specifications": {
                "type": "Mechanical (Gateron G Pro Brown)",
                "connectivity": "Bluetooth 5.1, USB-C wired",
                "backlight": "White LED",
                "battery": "4000 mAh, up to 200 hours",
                "layout": "TKL (87 keys)",
                "hot_swappable": "Yes",
                "features": "QMK/VIA, macOS + Windows keycaps"
            },
            "inventory": 35
        },
        {
            "name": "Ornata V3",
            "description": "Mecha-membrane gaming keyboard combining membrane comfort with mechanical click. Wrist rest included.",
            "brand": "Razer",
            "price": 6499.00,
            "rating": 4.2,
            "warranty": "2 Years",
            "specifications": {
                "type": "Mecha-Membrane",
                "connectivity": "USB-A wired",
                "backlight": "Razer Chroma RGB, per-key",
                "layout": "Full-size",
                "features": "Magnetic wrist rest, 10-key rollover, media keys"
            },
            "inventory": 45
        },
        {
            "name": "BlackWidow V4 75%",
            "description": "Compact 75% mechanical keyboard with Razer Orange switches for quiet tactile feedback.",
            "brand": "Razer",
            "price": 13999.00,
            "rating": 4.5,
            "warranty": "2 Years",
            "specifications": {
                "type": "Mechanical (Razer Orange Tactile)",
                "connectivity": "USB-C wired",
                "backlight": "Razer Chroma RGB, per-key",
                "layout": "75% compact",
                "hot_swappable": "Yes",
                "features": "Rotary knob, sound dampening foam, gasket-mount"
            },
            "inventory": 28
        },
    ],
    "mice": [
        {
            "name": "MX Master 3S",
            "description": "Ergonomic wireless mouse with MagSpeed scroll wheel and 8K DPI tracking. The gold standard for productivity.",
            "brand": "Logitech",
            "price": 8995.00,
            "rating": 4.7,
            "warranty": "2 Years",
            "specifications": {
                "sensor": "Darkfield 8000 DPI",
                "connectivity": "Bluetooth, USB receiver (Logi Bolt)",
                "battery": "Rechargeable, 70 days",
                "buttons": "7 programmable",
                "features": "MagSpeed scroll, Quiet clicks, Flow cross-computer, USB-C charging"
            },
            "inventory": 30
        },
        {
            "name": "G Pro X Superlight 2",
            "description": "Ultra-light wireless gaming mouse at just 60g. HERO 2 sensor with 44K DPI and 0.1ms click latency.",
            "brand": "Logitech",
            "price": 12995.00,
            "rating": 4.8,
            "warranty": "2 Years",
            "specifications": {
                "sensor": "HERO 2, 44000 DPI",
                "connectivity": "LIGHTSPEED Wireless, USB-C",
                "battery": "Rechargeable, 95 hours",
                "weight": "60g",
                "buttons": "5",
                "features": "PTFE feet, Zero-additive PTFE, Optical switches"
            },
            "inventory": 18
        },
        {
            "name": "DeathAdder V3",
            "description": "Iconic ergonomic gaming mouse redesigned. Ultra-light 59g with Focus Pro 30K sensor.",
            "brand": "Razer",
            "price": 7499.00,
            "rating": 4.5,
            "warranty": "2 Years",
            "specifications": {
                "sensor": "Focus Pro 30K",
                "connectivity": "USB-C wired",
                "weight": "59g",
                "buttons": "5",
                "switches": "Gen-3 Optical, 90M clicks",
                "features": "Speedflex cable, PTFE feet"
            },
            "inventory": 25
        },
        {
            "name": "Viper V3 Pro",
            "description": "Ambidextrous wireless gaming mouse with symmetrical design. Built for esports with 8000Hz polling.",
            "brand": "Razer",
            "price": 14999.00,
            "rating": 4.6,
            "warranty": "2 Years",
            "specifications": {
                "sensor": "Focus Pro 30K",
                "connectivity": "HyperSpeed Wireless, USB-C",
                "battery": "Rechargeable, 95 hours",
                "weight": "54g",
                "polling": "Up to 8000Hz (with dongle)",
                "buttons": "5 + 1 DPI button"
            },
            "inventory": 15
        },
        {
            "name": "Orochi V2",
            "description": "Ultra-compact wireless mouse for on-the-go gaming. Dual wireless modes with long battery life.",
            "brand": "Razer",
            "price": 4999.00,
            "rating": 4.3,
            "warranty": "2 Years",
            "specifications": {
                "sensor": "5G Advanced 18K DPI",
                "connectivity": "HyperSpeed Wireless, Bluetooth",
                "battery": "AA/AAA (425 hours wireless, 950 hours BT)",
                "weight": "60g (without battery)",
                "buttons": "6",
                "features": "Compact form, dual wireless"
            },
            "inventory": 40
        },
    ],
    "smartwatches": [
        {
            "name": "Galaxy Watch 6 Classic",
            "description": "Premium smartwatch with rotating bezel, advanced health monitoring, and Wear OS integration.",
            "brand": "Samsung",
            "price": 29999.00,
            "rating": 4.5,
            "warranty": "1 Year Manufacturer",
            "specifications": {
                "display": "1.47-inch Super AMOLED, 480x480",
                "processor": "Exynos W930",
                "storage": "16 GB",
                "battery": "425 mAh, up to 40 hours",
                "connectivity": "Bluetooth 5.3, Wi-Fi, NFC, LTE (optional)",
                "sensors": "BioActive, Temperature, SpO2, ECG",
                "os": "Wear OS 4, One UI Watch 5",
                "water_resistance": "5ATM + IP68"
            },
            "inventory": 20
        },
        {
            "name": "Apple Watch SE (2nd Gen)",
            "description": "Affordable Apple Watch with core health features, crash detection, and seamless iPhone integration.",
            "brand": "Apple",
            "price": 29900.00,
            "rating": 4.4,
            "warranty": "1 Year Apple Limited",
            "specifications": {
                "display": "44mm Retina LTPO OLED",
                "processor": "Apple S8",
                "storage": "32 GB",
                "battery": "Up to 18 hours",
                "connectivity": "Bluetooth 5.3, Wi-Fi, NFC",
                "sensors": "Heart rate, Accelerometer, Gyroscope",
                "os": "watchOS 10",
                "water_resistance": "WR50 (50m)"
            },
            "inventory": 25
        },
        {
            "name": "GTR 4",
            "description": "Feature-rich smartwatch with dual-band GPS, 14-day battery life, and 150+ sports modes.",
            "brand": "Amazfit",
            "price": 14999.00,
            "rating": 4.3,
            "warranty": "1 Year Manufacturer",
            "specifications": {
                "display": "1.43-inch AMOLED, 466x466",
                "battery": "475 mAh, up to 14 days",
                "connectivity": "Bluetooth 5.2, Wi-Fi, NFC (select markets)",
                "gps": "Dual-band GPS (5 satellite systems)",
                "sensors": "BioTracker 4.0 PPG, SpO2",
                "sports_modes": "150+",
                "os": "Zepp OS 2.0",
                "water_resistance": "5 ATM"
            },
            "inventory": 35
        },
        {
            "name": "Band 8",
            "description": "Ultra-slim fitness band with AMOLED display and 2-week battery life. Over 150 workout modes.",
            "brand": "Huawei",
            "price": 4499.00,
            "rating": 4.1,
            "warranty": "1 Year Manufacturer",
            "specifications": {
                "display": "1.47-inch AMOLED, 194x368",
                "battery": "Up to 14 days",
                "connectivity": "Bluetooth 5.0",
                "sensors": "Heart rate, SpO2, Accelerometer",
                "sports_modes": "100+",
                "weight": "14g (without strap)",
                "water_resistance": "5 ATM"
            },
            "inventory": 50
        },
        {
            "name": "Noise ColorFit Pro 5",
            "description": "Budget smartwatch with 1.85-inch display, Bluetooth calling, and AI health suite. Great value.",
            "brand": "Noise",
            "price": 2999.00,
            "rating": 3.8,
            "warranty": "1 Year Manufacturer",
            "specifications": {
                "display": "1.85-inch TFT LCD",
                "battery": "Up to 7 days",
                "connectivity": "Bluetooth 5.3",
                "calling": "Bluetooth calling with speaker/mic",
                "sensors": "Heart rate, SpO2",
                "sports_modes": "100+",
                "water_resistance": "IP68"
            },
            "inventory": 65
        },
    ],
}

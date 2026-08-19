"""
AgentCart — Product Catalog Expander & Sync Script.

Appends 40+ high-demand, modern tech products across all 7 categories
into the PostgreSQL database without wiping existing carts or orders.
"""

import asyncio
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from sqlalchemy import select
from app.database.connection import async_session_factory
from app.models import Category, Product, Inventory

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

NEW_PRODUCTS = {
    "laptops": [
        {
            "name": "MacBook Air M3 (13.6-inch)",
            "brand": "Apple",
            "price": 114900.0,
            "rating": 4.8,
            "description": "Apple M3 chip, 16GB Unified Memory, 512GB SSD, Liquid Retina Display, 18-Hour Battery Life, Midnight Color.",
            "specifications": {"processor": "Apple M3 (8-core CPU, 10-core GPU)", "ram": "16GB Unified", "storage": "512GB SSD", "display": "13.6-inch Liquid Retina", "weight": "1.24 kg"},
            "warranty": "1 Year Apple Limited Warranty",
            "inventory": 45,
        },
        {
            "name": "MacBook Pro 16 M3 Max",
            "brand": "Apple",
            "price": 349900.0,
            "rating": 4.9,
            "description": "Extreme workstation performance with Apple M3 Max (16-core CPU, 40-core GPU), 36GB Unified Memory, 1TB SSD, Liquid Retina XDR 120Hz.",
            "specifications": {"processor": "Apple M3 Max", "ram": "36GB Unified", "storage": "1TB NVMe SSD", "display": "16.2-inch Liquid Retina XDR (120Hz ProMotion)", "weight": "2.16 kg"},
            "warranty": "1 Year Apple Limited Warranty",
            "inventory": 20,
        },
        {
            "name": "Dell XPS 15 (9530)",
            "brand": "Dell",
            "price": 189990.0,
            "rating": 4.6,
            "description": "Intel Core i7-13700H, 16GB DDR5, 1TB SSD, NVIDIA GeForce RTX 4060 8GB, 15.6-inch 3.5K OLED Touch Display.",
            "specifications": {"processor": "Intel Core i7-13700H", "ram": "16GB DDR5", "storage": "1TB PCIe Gen4 SSD", "gpu": "NVIDIA GeForce RTX 4060 8GB", "display": "15.6-inch 3.5K OLED Touch"},
            "warranty": "1 Year Premium Onsite Support",
            "inventory": 30,
        },
        {
            "name": "Lenovo Legion Pro 7i",
            "brand": "Lenovo",
            "price": 239990.0,
            "rating": 4.7,
            "description": "Top-tier gaming laptop with Intel Core i9-14900HX, 32GB DDR5, 1TB Gen4 SSD, NVIDIA GeForce RTX 4080 12GB, 16-inch WQXGA 240Hz.",
            "specifications": {"processor": "Intel Core i9-14900HX", "ram": "32GB DDR5", "storage": "1TB SSD", "gpu": "NVIDIA GeForce RTX 4080 12GB", "display": "16-inch 240Hz 500nits G-SYNC"},
            "warranty": "1 Year Legion Ultimate Support",
            "inventory": 25,
        },
        {
            "name": "ASUS ZenBook Duo 14 OLED",
            "brand": "ASUS",
            "price": 159990.0,
            "rating": 4.5,
            "description": "Dual 14-inch 3K 120Hz OLED touchscreens, Intel Core Ultra 7 155H, 16GB LPDDR5X, 1TB SSD, Detachable Bluetooth Keyboard.",
            "specifications": {"processor": "Intel Core Ultra 7 155H", "ram": "16GB LPDDR5X", "storage": "1TB SSD", "display": "Dual 14-inch 3K 120Hz OLED", "weight": "1.35 kg"},
            "warranty": "1 Year Onsite Warranty",
            "inventory": 18,
        },
        {
            "name": "Acer Aspire Lite 15",
            "brand": "Acer",
            "price": 31990.0,
            "rating": 4.1,
            "description": "Budget essential laptop with Intel Core i3 12th Gen, 8GB RAM, 512GB SSD, 15.6-inch Full HD display, Windows 11 Home.",
            "specifications": {"processor": "Intel Core i3-1215U", "ram": "8GB DDR4", "storage": "512GB NVMe SSD", "display": "15.6-inch Full HD", "weight": "1.59 kg"},
            "warranty": "1 Year Carry-in Warranty",
            "inventory": 60,
        },
    ],
    "smartphones": [
        {
            "name": "iPhone 16 Pro Max",
            "brand": "Apple",
            "price": 144900.0,
            "rating": 4.9,
            "description": "A18 Pro Bionic chip, Grade 5 Titanium design, 48MP Fusion camera system with 5x Telephoto, 6.9-inch Super Retina XDR with Promotion.",
            "specifications": {"processor": "Apple A18 Pro", "storage": "256GB", "display": "6.9-inch OLED 120Hz", "camera": "48MP Main + 48MP Ultra-wide + 12MP 5x Telephoto"},
            "warranty": "1 Year Apple Warranty",
            "inventory": 40,
        },
        {
            "name": "Samsung Galaxy S24 Ultra",
            "brand": "Samsung",
            "price": 129999.0,
            "rating": 4.8,
            "description": "Snapdragon 8 Gen 3 for Galaxy, Galaxy AI built-in, Titanium frame, 200MP Quad Telephoto Camera, 6.8-inch Dynamic AMOLED 2X 2600 nits, S Pen.",
            "specifications": {"processor": "Snapdragon 8 Gen 3", "ram": "12GB", "storage": "256GB", "display": "6.8-inch QHD+ 120Hz AMOLED", "battery": "5000 mAh"},
            "warranty": "1 Year Manufacturer Warranty",
            "inventory": 50,
        },
        {
            "name": "Google Pixel 9 Pro",
            "brand": "Google",
            "price": 106999.0,
            "rating": 4.7,
            "description": "Google Tensor G4 with advanced Gemini AI, Super Actua display, Pro camera triple lens system with 30x Super Res Zoom, 7 years of OS updates.",
            "specifications": {"processor": "Google Tensor G4", "ram": "16GB", "storage": "128GB", "display": "6.3-inch LTPO OLED 120Hz", "camera": "50MP + 48MP + 48MP"},
            "warranty": "1 Year Google Warranty",
            "inventory": 35,
        },
        {
            "name": "OnePlus 12",
            "brand": "OnePlus",
            "price": 64999.0,
            "rating": 4.6,
            "description": "Snapdragon 8 Gen 3, 16GB LPDDR5X RAM, 512GB UFS 4.0, 4th Gen Hasselblad Camera for Mobile, 5400 mAh Battery with 100W SUPERVOOC charging.",
            "specifications": {"processor": "Snapdragon 8 Gen 3", "ram": "16GB", "storage": "512GB", "charging": "100W Wired, 50W Wireless", "display": "6.82-inch 2K ProXDR 120Hz"},
            "warranty": "1 Year OnePlus Warranty",
            "inventory": 55,
        },
        {
            "name": "Nothing Phone (2)",
            "brand": "Nothing",
            "price": 39999.0,
            "rating": 4.4,
            "description": "Iconic transparent design with Glyph Interface, Snapdragon 8+ Gen 1, 50MP dual rear cameras with Sony IMX890, 6.7-inch flexible LTPO OLED.",
            "specifications": {"processor": "Snapdragon 8+ Gen 1", "ram": "12GB", "storage": "256GB", "display": "6.7-inch OLED 120Hz", "battery": "4700 mAh"},
            "warranty": "1 Year Manufacturer Warranty",
            "inventory": 40,
        },
    ],
    "headphones": [
        {
            "name": "Bose QuietComfort Ultra",
            "brand": "Bose",
            "price": 35900.0,
            "rating": 4.8,
            "description": "World-class noise cancellation, breakthrough Spatial Audio immersion, CustomTune technology, up to 24 hours battery life.",
            "specifications": {"type": "Over-Ear Wireless", "battery": "24 Hours", "noise_cancellation": "Active (CustomTune)", "connectivity": "Bluetooth 5.3, Multipoint"},
            "warranty": "1 Year Bose Warranty",
            "inventory": 30,
        },
        {
            "name": "AirPods Max",
            "brand": "Apple",
            "price": 59900.0,
            "rating": 4.7,
            "description": "High-fidelity audio with Apple H1 headphone chip, Computational Audio, Industry-leading Active Noise Cancellation with Transparency mode, Space Grey.",
            "specifications": {"driver": "Apple-designed 40mm dynamic driver", "battery": "20 Hours with ANC", "chip": "Apple H1 in each cup"},
            "warranty": "1 Year Apple Warranty",
            "inventory": 25,
        },
        {
            "name": "Sony WF-1000XM5 Earbuds",
            "brand": "Sony",
            "price": 19990.0,
            "rating": 4.6,
            "description": "Industry-leading noise canceling earbuds with Integrated Processor V2 and HD Noise Canceling Processor QN2e, LDAC Hi-Res Wireless, 24-hour battery.",
            "specifications": {"type": "In-Ear True Wireless", "anc": "Dual processor HD ANC", "battery": "8h earbuds + 16h case", "waterproof": "IPX4"},
            "warranty": "1 Year Sony Warranty",
            "inventory": 45,
        },
        {
            "name": "Marshall Major IV Wireless",
            "brand": "Marshall",
            "price": 11999.0,
            "rating": 4.5,
            "description": "Iconic vintage rock design with 80+ solid hours of wireless playtime, custom-tuned dynamic drivers, wireless charging support.",
            "specifications": {"battery": "80+ Hours", "charging": "Wireless & USB-C Fast Charge", "drivers": "40mm Dynamic", "weight": "165 g"},
            "warranty": "1 Year Manufacturer Warranty",
            "inventory": 35,
        },
        {
            "name": "Realme Buds Air 5 Pro",
            "brand": "Realme",
            "price": 4499.0,
            "rating": 4.3,
            "description": "Flagship-grade 50dB Active Noise Cancellation, RealBoost Dual Drivers (11mm bass + 6mm planar tweeter), LDAC Hi-Res Audio, 40 hours playtime.",
            "specifications": {"anc": "50dB Deep Sea ANC", "codecs": "LDAC, AAC, SBC", "battery": "40 Hours total", "latency": "40ms ultra-low"},
            "warranty": "1 Year Brand Warranty",
            "inventory": 80,
        },
    ],
    "monitors": [
        {
            "name": "Dell UltraSharp 32 4K USB-C Hub (U3223QE)",
            "brand": "Dell",
            "price": 84990.0,
            "rating": 4.8,
            "description": "31.5-inch 4K UHD (3840x2160) monitor with groundbreaking IPS Black technology, 2000:1 contrast ratio, 90W USB-C Power Delivery, RJ45 Ethernet.",
            "specifications": {"resolution": "3840 x 2160 (4K)", "panel": "IPS Black 60Hz", "color_gamut": "98% DCI-P3, 100% sRGB", "ports": "USB-C with 90W PD, DisplayPort, HDMI, RJ45"},
            "warranty": "3 Years Dell Advanced Exchange Service",
            "inventory": 20,
        },
        {
            "name": "Samsung Odyssey OLED G9 (49-inch)",
            "brand": "Samsung",
            "price": 149999.0,
            "rating": 4.9,
            "description": "49-inch Dual QHD (5120x1440) 32:9 curved gaming monitor, Neo Quantum Processor Pro, 240Hz refresh rate, 0.03ms response time, DisplayHDR True Black 400.",
            "specifications": {"size": "49-inch 1800R Curved", "resolution": "5120 x 1440 Dual QHD", "refresh_rate": "240Hz", "response_time": "0.03ms (GtG)"},
            "warranty": "3 Years Samsung Warranty",
            "inventory": 12,
        },
        {
            "name": "LG UltraFine 27 4K UHD (27UN880)",
            "brand": "LG",
            "price": 34999.0,
            "rating": 4.6,
            "description": "27-inch 4K UHD IPS display with Ergonomic Stand (C-Clamp arm), HDR10, sRGB 99%, USB-C with 60W Power Delivery.",
            "specifications": {"resolution": "3840 x 2160", "panel": "IPS", "stand": "Ergo Arm (Extend/Retract/Swivel/Pivot)", "ports": "USB-C, HDMI x2, DisplayPort"},
            "warranty": "3 Years LG Onsite Warranty",
            "inventory": 35,
        },
        {
            "name": "Acer Nitro 27-inch WQHD 180Hz",
            "brand": "Acer",
            "price": 16999.0,
            "rating": 4.4,
            "description": "27-inch 2560x1440 WQHD Fast IPS gaming monitor, 180Hz overclocked refresh rate, 0.5ms response time, AMD FreeSync Premium, HDR10.",
            "specifications": {"resolution": "2560 x 1440 2K", "refresh_rate": "180Hz", "response_time": "0.5ms", "panel": "Fast IPS"},
            "warranty": "3 Years Acer Onsite Warranty",
            "inventory": 50,
        },
    ],
    "keyboards": [
        {
            "name": "Keychron Q1 Pro Wireless Mechanical",
            "brand": "Keychron",
            "price": 18999.0,
            "rating": 4.8,
            "description": "Full CNC aluminum body, 75% layout, Double-Gasket mount, QMK/VIA programmable, Bluetooth 5.1 & Type-C, Hot-Swappable Keychron K Pro Switches.",
            "specifications": {"layout": "75%", "switches": "Keychron K Pro Banana (Tactile)", "connectivity": "Bluetooth 5.1 / Type-C Wired", "body": "Full CNC Aluminum"},
            "warranty": "1 Year Keychron Warranty",
            "inventory": 25,
        },
        {
            "name": "Logitech MX Mechanical Wireless",
            "brand": "Logitech",
            "price": 14995.0,
            "rating": 4.7,
            "description": "Low-profile mechanical keyboard with Tactile Quiet switches, Smart Illumination backlighting, Easy-Switch for up to 3 devices, Logi Bolt USB & Bluetooth.",
            "specifications": {"switches": "Low Profile Tactile Quiet", "battery": "Up to 15 days (10 months with backlighting off)", "compatibility": "Windows, macOS, Linux, ChromeOS"},
            "warranty": "2 Years Logitech Warranty",
            "inventory": 40,
        },
        {
            "name": "NuPhy Air75 V2 Wireless Mechanical",
            "brand": "NuPhy",
            "price": 12499.0,
            "rating": 4.7,
            "description": "Ultra-slim 75% low-profile wireless mechanical keyboard with 1000Hz polling rate in 2.4G, QMK/VIA support, Gateron Low Profile Switches, RGB backlighting.",
            "specifications": {"layout": "75%", "thickness": "13.5mm ultra-thin", "battery": "4000 mAh", "switches": "Gateron Low-Profile Cowberry"},
            "warranty": "1 Year Brand Warranty",
            "inventory": 30,
        },
        {
            "name": "Royal Kludge RK84 75% Mechanical",
            "brand": "Royal Kludge",
            "price": 4999.0,
            "rating": 4.3,
            "description": "Budget custom mechanical keyboard with Triple Mode (Bluetooth 5.0 / 2.4G / Type-C), Hot-Swappable PCB, White Backlit, 3750 mAh high-capacity battery.",
            "specifications": {"layout": "84 Keys (75%)", "switches": "RK Brown (Hot-Swappable)", "connectivity": "Triple Mode (BT/2.4G/USB-C)"},
            "warranty": "1 Year Warranty",
            "inventory": 65,
        },
    ],
    "mice": [
        {
            "name": "Logitech MX Master 3S Performance",
            "brand": "Logitech",
            "price": 8995.0,
            "rating": 4.9,
            "description": "Quiet Clicks with 8000 DPI Darkfield tracking (works on glass), MagSpeed Electromagnetic Scrolling (1000 lines/sec), ergonomic thumb rest with gesture button.",
            "specifications": {"dpi": "8000 DPI Darkfield", "battery": "Up to 70 days per full charge", "connectivity": "Bluetooth & Logi Bolt", "weight": "141 g"},
            "warranty": "2 Years Logitech Warranty",
            "inventory": 50,
        },
        {
            "name": "Logitech G Pro X Superlight 2",
            "brand": "Logitech",
            "price": 14995.0,
            "rating": 4.8,
            "description": "Ultra-lightweight 60g wireless esports mouse, HERO 2 Sensor with 32,000 DPI, 2000Hz polling rate, LIGHTFORCE hybrid optical-mechanical switches.",
            "specifications": {"weight": "60 grams", "sensor": "HERO 2 (32,000 DPI)", "polling_rate": "2000Hz LIGHTSPEED", "battery": "95 Hours"},
            "warranty": "2 Years Logitech Warranty",
            "inventory": 35,
        },
        {
            "name": "Razer DeathAdder V3 Pro Wireless",
            "brand": "Razer",
            "price": 12999.0,
            "rating": 4.7,
            "description": "Ergonomic 63g esports gaming mouse, Focus Pro 30K Optical Sensor, Gen-3 Optical Mouse Switches (90M click lifecycle), 90 hours battery life.",
            "specifications": {"weight": "63 grams", "sensor": "Focus Pro 30K Optical", "battery": "90 Hours"},
            "warranty": "2 Years Razer Warranty",
            "inventory": 30,
        },
    ],
    "smartwatches": [
        {
            "name": "Apple Watch Ultra 2 (49mm)",
            "brand": "Apple",
            "price": 89900.0,
            "rating": 4.9,
            "description": "Titanium case with Sapphire crystal display, 3000 nits peak brightness, S9 SiP with Double Tap gesture, Precision Dual-Frequency GPS, 36-hour battery (72h in low power).",
            "specifications": {"case": "49mm Aerospace-grade Titanium", "display": "OLED 3000 nits", "water_resistance": "100m (EN13319 Dive Certified)", "gps": "L1 & L5 Dual-Frequency"},
            "warranty": "1 Year Apple Warranty",
            "inventory": 20,
        },
        {
            "name": "Samsung Galaxy Watch 6 Classic (47mm LTE)",
            "brand": "Samsung",
            "price": 36999.0,
            "rating": 4.6,
            "description": "Physical Rotating Bezel, Sapphire Crystal Super AMOLED display, BioActive Sensor (ECG, Blood Pressure, BIA Body Composition), Wear OS Powered by Samsung.",
            "specifications": {"case": "47mm Stainless Steel", "display": "1.5-inch Super AMOLED 2000 nits", "connectivity": "4G LTE, Bluetooth 5.3, NFC, GPS"},
            "warranty": "1 Year Samsung Warranty",
            "inventory": 30,
        },
        {
            "name": "OnePlus Watch 2",
            "brand": "OnePlus",
            "price": 21999.0,
            "rating": 4.7,
            "description": "Dual-Engine Architecture (Snapdragon W5 + BES2700), up to 100 hours of battery life in Smart Mode, 1.43-inch AMOLED, Stainless Steel chassis with Sapphire Crystal.",
            "specifications": {"battery": "100 Hours (4 days) Smart Mode", "os": "Wear OS 4 by Google", "chips": "Snapdragon W5 + BES2700 MCU", "water_resistance": "5ATM + IP68 + MIL-STD-810H"},
            "warranty": "1 Year OnePlus Warranty",
            "inventory": 40,
        },
        {
            "name": "Noise ColorFit Pro 5 Max",
            "brand": "Noise",
            "price": 3999.0,
            "rating": 4.2,
            "description": "1.96-inch AMOLED display, BT Calling with TruSync, Post-training VO2 max & recovery analysis, Rapid SOS feature, 100+ sports modes.",
            "specifications": {"display": "1.96-inch AMOLED", "battery": "Up to 7 days", "sensors": "Heart Rate, SpO2, Sleep Tracker, Stress Monitor"},
            "warranty": "1 Year Brand Warranty",
            "inventory": 90,
        },
    ],
}


async def sync_new_products():
    """Sync all new products into PostgreSQL database."""
    async with async_session_factory() as session:
        # Load category map
        cat_stmt = select(Category)
        res = await session.execute(cat_stmt)
        categories = {c.slug: c for c in res.scalars().all()}

        added_count = 0
        for cat_slug, prod_list in NEW_PRODUCTS.items():
            category = categories.get(cat_slug)
            if not category:
                logger.warning(f"Category {cat_slug} not found. Skipping.")
                continue

            for prod_data in prod_list:
                # Check if product already exists by name
                existing_stmt = select(Product).where(Product.name == prod_data["name"])
                existing_prod = (await session.execute(existing_stmt)).scalars().first()
                if existing_prod:
                    continue  # Already exists

                inv_qty = prod_data.get("inventory", 50)
                product = Product(
                    name=prod_data["name"],
                    description=prod_data["description"],
                    brand=prod_data["brand"],
                    category_id=category.id,
                    price=prod_data["price"],
                    rating=prod_data["rating"],
                    specifications=prod_data.get("specifications"),
                    warranty=prod_data.get("warranty"),
                    image_url=None,
                )
                session.add(product)
                await session.flush()

                # Add inventory
                inv = Inventory(product_id=product.id, quantity=inv_qty)
                session.add(inv)
                added_count += 1
                logger.info(f"➕ Added: {product.name} (₹{product.price:,.0f}) in {category.name}")

        await session.commit()
        logger.info(f"\n🎉 Sync complete! Added {added_count} new products to catalog.")


if __name__ == "__main__":
    asyncio.run(sync_new_products())

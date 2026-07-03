# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Curated destination catalog for itinerary recommendations.

MVP: Returns curated sample data with IDR pricing. Future: integrate live
POI/activity inventory (Amadeus, Viator, GetYourGuide APIs).
"""

from google.adk.tools import ToolContext

DESTINATION_CATALOG: dict[str, dict] = {
    "bali": {
        "name": "Bali",
        "country": "Indonesia",
        "region": "Southeast Asia",
        "domestic_for_indonesia": True,
        "themes": [
            "beach",
            "culture",
            "nature",
            "romantic",
            "family",
            "budget",
            "luxury",
        ],
        "companions": ["couple", "family", "solo", "friends"],
        "best_seasons": ["dry season (April-October)"],
        "seasonal_highlights": {
            "dry": "Best beach and volcano-trekking weather, Galungan festivals",
        },
        "activities": [
            {
                "name": "Uluwatu Temple sunset & Kecak dance",
                "price_idr": 150000,
                "duration_hours": 3,
                "tags": ["culture", "romantic", "family"],
            },
            {
                "name": "Tegallalang Rice Terrace walk",
                "price_idr": 25000,
                "duration_hours": 2,
                "tags": ["nature", "budget", "family"],
            },
            {
                "name": "Ubud Sacred Monkey Forest",
                "price_idr": 80000,
                "duration_hours": 2,
                "tags": ["nature", "family"],
            },
            {
                "name": "Mount Batur sunrise trek with breakfast",
                "price_idr": 450000,
                "duration_hours": 6,
                "tags": ["nature", "adventure", "solo"],
            },
            {
                "name": "Nusa Penida day trip (Kelingking Beach)",
                "price_idr": 750000,
                "duration_hours": 10,
                "tags": ["beach", "adventure", "couple"],
            },
            {
                "name": "Jimbaran Bay seafood sunset dinner",
                "price_idr": 400000,
                "duration_hours": 2,
                "tags": ["romantic", "couple", "food"],
            },
            {
                "name": "Balinese spa & massage (couples package)",
                "price_idr": 500000,
                "duration_hours": 2,
                "tags": ["romantic", "couple", "relaxation"],
            },
            {
                "name": "Waterbom Bali waterpark",
                "price_idr": 535000,
                "duration_hours": 5,
                "tags": ["family", "kids"],
            },
            {
                "name": "Kuta Beach & Seminyak sunset walk",
                "price_idr": 0,
                "duration_hours": 3,
                "tags": ["beach", "budget", "free"],
            },
        ],
        "hotels": [
            {
                "name": "Ubud family guesthouse",
                "tier": "budget",
                "price_idr_per_night": 250000,
                "tags": ["budget", "solo"],
            },
            {
                "name": "Seminyak 4-star resort with kids club",
                "tier": "mid",
                "price_idr_per_night": 900000,
                "tags": ["family", "couple"],
            },
            {
                "name": "Nusa Dua 5-star beachfront villa with private pool",
                "tier": "luxury",
                "price_idr_per_night": 3500000,
                "tags": ["luxury", "romantic"],
            },
        ],
        "daily_food_cost_idr": {"budget": 150000, "mid": 400000, "luxury": 1200000},
        "local_transport_cost_idr_per_day": 150000,
    },
    "labuan_bajo": {
        "name": "Labuan Bajo",
        "country": "Indonesia",
        "region": "Southeast Asia",
        "domestic_for_indonesia": True,
        "themes": ["nature", "adventure", "beach", "romantic"],
        "companions": ["couple", "solo", "friends", "family"],
        "best_seasons": ["dry season (April-June, September-November)"],
        "seasonal_highlights": {
            "dry": "Calm seas for Komodo sailing trips, best visibility for diving",
        },
        "activities": [
            {
                "name": "Komodo National Park day cruise (dragons + trekking)",
                "price_idr": 1500000,
                "duration_hours": 12,
                "tags": ["nature", "adventure", "wildlife"],
            },
            {
                "name": "Padar Island sunrise hike",
                "price_idr": 300000,
                "duration_hours": 4,
                "tags": ["nature", "adventure", "photo"],
            },
            {
                "name": "Pink Beach snorkeling",
                "price_idr": 350000,
                "duration_hours": 4,
                "tags": ["beach", "snorkeling", "family"],
            },
            {
                "name": "Manta Point snorkeling with manta rays",
                "price_idr": 500000,
                "duration_hours": 5,
                "tags": ["adventure", "snorkeling"],
            },
            {
                "name": "Rangko Cave swim",
                "price_idr": 250000,
                "duration_hours": 3,
                "tags": ["nature", "adventure"],
            },
            {
                "name": "Sunset at Paradise Bar Bukit Silvia",
                "price_idr": 100000,
                "duration_hours": 2,
                "tags": ["romantic", "budget", "couple"],
            },
            {
                "name": "Cunca Wulang waterfall trek",
                "price_idr": 200000,
                "duration_hours": 5,
                "tags": ["nature", "solo"],
            },
        ],
        "hotels": [
            {
                "name": "Harbourside backpacker hostel",
                "tier": "budget",
                "price_idr_per_night": 300000,
                "tags": ["budget", "solo"],
            },
            {
                "name": "Hilltop 4-star hotel with bay view",
                "tier": "mid",
                "price_idr_per_night": 1100000,
                "tags": ["couple", "family"],
            },
            {
                "name": "Private island eco-resort (Komodo view)",
                "tier": "luxury",
                "price_idr_per_night": 4500000,
                "tags": ["luxury", "romantic"],
            },
        ],
        "daily_food_cost_idr": {"budget": 150000, "mid": 350000, "luxury": 900000},
        "local_transport_cost_idr_per_day": 200000,
    },
    "singapore": {
        "name": "Singapore",
        "country": "Singapore",
        "region": "Southeast Asia",
        "domestic_for_indonesia": False,
        "themes": ["city", "family", "luxury", "food", "shopping"],
        "companions": ["family", "couple", "solo", "friends"],
        "best_seasons": ["year-round (February-April driest)"],
        "seasonal_highlights": {
            "year_round": "Indoor attractions unaffected by weather; Great Singapore Sale mid-year",
        },
        "activities": [
            {
                "name": "Gardens by the Bay (Cloud Forest + Flower Dome)",
                "price_idr": 380000,
                "duration_hours": 4,
                "tags": ["nature", "family", "photo"],
            },
            {
                "name": "Marina Bay Sands SkyPark observation deck",
                "price_idr": 330000,
                "duration_hours": 2,
                "tags": ["city", "luxury", "photo"],
            },
            {
                "name": "Universal Studios Singapore",
                "price_idr": 980000,
                "duration_hours": 8,
                "tags": ["family", "kids", "theme_park"],
            },
            {
                "name": "Singapore Zoo / River Wonders",
                "price_idr": 550000,
                "duration_hours": 5,
                "tags": ["family", "kids", "wildlife"],
            },
            {
                "name": "Hawker centre food crawl (Maxwell / Lau Pa Sat)",
                "price_idr": 120000,
                "duration_hours": 3,
                "tags": ["food", "budget", "local"],
            },
            {
                "name": "Merlion Park & Marina Bay waterfront walk",
                "price_idr": 0,
                "duration_hours": 2,
                "tags": ["city", "budget", "free"],
            },
            {
                "name": "Fine dining at a Michelin-starred restaurant",
                "price_idr": 2500000,
                "duration_hours": 3,
                "tags": ["luxury", "food", "romantic"],
            },
            {
                "name": "Sentosa beaches & cable car",
                "price_idr": 400000,
                "duration_hours": 5,
                "tags": ["beach", "family"],
            },
            {
                "name": "CE LA VI rooftop bar at Marina Bay Sands",
                "price_idr": 600000,
                "duration_hours": 2,
                "tags": ["luxury", "nightlife", "couple"],
            },
        ],
        "hotels": [
            {
                "name": "Chinatown capsule hotel",
                "tier": "budget",
                "price_idr_per_night": 600000,
                "tags": ["budget", "solo"],
            },
            {
                "name": "Orchard Road 4-star hotel",
                "tier": "mid",
                "price_idr_per_night": 2200000,
                "tags": ["family", "shopping"],
            },
            {
                "name": "Marina Bay Sands (infinity pool access)",
                "tier": "luxury",
                "price_idr_per_night": 7500000,
                "tags": ["luxury", "iconic", "romantic"],
            },
        ],
        "daily_food_cost_idr": {"budget": 250000, "mid": 600000, "luxury": 2000000},
        "local_transport_cost_idr_per_day": 120000,
    },
    "seoul": {
        "name": "Seoul",
        "country": "South Korea",
        "region": "East Asia",
        "domestic_for_indonesia": False,
        "themes": ["culture", "city", "food", "shopping", "history", "sakura"],
        "companions": ["solo", "couple", "family", "friends"],
        "best_seasons": [
            "spring (April-May, cherry blossoms)",
            "autumn (October-November, foliage)",
        ],
        "seasonal_highlights": {
            "spring": "Cherry blossoms at Yeouido Park and Seokchon Lake (early-mid April)",
            "autumn": "Fall foliage at Nami Island and palace gardens",
            "winter": "Ski resorts nearby, festive markets",
        },
        "activities": [
            {
                "name": "Gyeongbokgung Palace + royal guard ceremony",
                "price_idr": 40000,
                "duration_hours": 3,
                "tags": ["culture", "history", "solo", "budget"],
            },
            {
                "name": "Hanbok rental & Bukchon Hanok Village walk",
                "price_idr": 250000,
                "duration_hours": 4,
                "tags": ["culture", "photo", "solo", "couple"],
            },
            {
                "name": "Traditional tea ceremony in Insadong",
                "price_idr": 180000,
                "duration_hours": 2,
                "tags": ["culture", "local", "solo"],
            },
            {
                "name": "Korean cooking class (kimchi + bulgogi)",
                "price_idr": 550000,
                "duration_hours": 3,
                "tags": ["food", "local", "solo", "culture"],
            },
            {
                "name": "DMZ half-day tour",
                "price_idr": 700000,
                "duration_hours": 6,
                "tags": ["history", "solo"],
            },
            {
                "name": "N Seoul Tower & Namsan cable car",
                "price_idr": 260000,
                "duration_hours": 3,
                "tags": ["city", "romantic", "couple"],
            },
            {
                "name": "Gwangjang Market street food tour",
                "price_idr": 200000,
                "duration_hours": 3,
                "tags": ["food", "budget", "local"],
            },
            {
                "name": "Yeouido cherry blossom festival walk (spring)",
                "price_idr": 0,
                "duration_hours": 3,
                "tags": ["sakura", "spring", "free", "photo"],
            },
            {
                "name": "K-pop & Hongdae street culture evening",
                "price_idr": 150000,
                "duration_hours": 4,
                "tags": ["city", "solo", "friends"],
            },
        ],
        "hotels": [
            {
                "name": "Hongdae guesthouse (solo-friendly)",
                "tier": "budget",
                "price_idr_per_night": 450000,
                "tags": ["budget", "solo"],
            },
            {
                "name": "Myeongdong 4-star hotel",
                "tier": "mid",
                "price_idr_per_night": 1500000,
                "tags": ["shopping", "family"],
            },
            {
                "name": "Signiel Seoul (Lotte World Tower)",
                "tier": "luxury",
                "price_idr_per_night": 6000000,
                "tags": ["luxury", "city_view"],
            },
        ],
        "daily_food_cost_idr": {"budget": 250000, "mid": 500000, "luxury": 1500000},
        "local_transport_cost_idr_per_day": 100000,
    },
    "tokyo_kyoto": {
        "name": "Tokyo & Kyoto",
        "country": "Japan",
        "region": "East Asia",
        "domestic_for_indonesia": False,
        "themes": ["culture", "city", "food", "history", "sakura", "nature"],
        "companions": ["solo", "couple", "family", "friends"],
        "best_seasons": [
            "spring (late March-early April, sakura)",
            "autumn (November, foliage)",
        ],
        "seasonal_highlights": {
            "spring": "Sakura full bloom: Ueno Park & Meguro River (Tokyo), Maruyama Park & Philosopher's Path (Kyoto), late March-early April",
            "autumn": "Red maple foliage at Kyoto temples",
        },
        "activities": [
            {
                "name": "Ueno Park & Shinjuku Gyoen sakura hanami picnic",
                "price_idr": 55000,
                "duration_hours": 4,
                "tags": ["sakura", "spring", "budget", "photo"],
            },
            {
                "name": "Meguro River evening sakura illumination",
                "price_idr": 0,
                "duration_hours": 2,
                "tags": ["sakura", "spring", "free", "romantic"],
            },
            {
                "name": "Senso-ji Temple & Asakusa old town",
                "price_idr": 0,
                "duration_hours": 3,
                "tags": ["culture", "history", "free"],
            },
            {
                "name": "teamLab Planets digital art museum",
                "price_idr": 420000,
                "duration_hours": 3,
                "tags": ["city", "photo", "family"],
            },
            {
                "name": "Shinkansen day trip Tokyo-Kyoto (round trip)",
                "price_idr": 3200000,
                "duration_hours": 3,
                "tags": ["transport", "experience"],
            },
            {
                "name": "Fushimi Inari shrine torii gate hike",
                "price_idr": 0,
                "duration_hours": 3,
                "tags": ["culture", "free", "photo", "solo"],
            },
            {
                "name": "Kinkaku-ji (Golden Pavilion) & zen gardens",
                "price_idr": 55000,
                "duration_hours": 2,
                "tags": ["culture", "history", "budget"],
            },
            {
                "name": "Kaiseki dinner in Gion with geisha district walk",
                "price_idr": 1800000,
                "duration_hours": 3,
                "tags": ["luxury", "food", "romantic", "culture"],
            },
            {
                "name": "Tsukiji outer market sushi breakfast",
                "price_idr": 300000,
                "duration_hours": 2,
                "tags": ["food", "local"],
            },
        ],
        "hotels": [
            {
                "name": "Asakusa capsule hotel / hostel",
                "tier": "budget",
                "price_idr_per_night": 500000,
                "tags": ["budget", "solo"],
            },
            {
                "name": "Shinjuku 4-star hotel",
                "tier": "mid",
                "price_idr_per_night": 2000000,
                "tags": ["family", "couple"],
            },
            {
                "name": "Park Hyatt Tokyo / Kyoto ryokan with onsen",
                "tier": "luxury",
                "price_idr_per_night": 8000000,
                "tags": ["luxury", "romantic"],
            },
        ],
        "daily_food_cost_idr": {"budget": 300000, "mid": 650000, "luxury": 2000000},
        "local_transport_cost_idr_per_day": 150000,
    },
    "melbourne": {
        "name": "Melbourne",
        "country": "Australia",
        "region": "Oceania",
        "domestic_for_indonesia": False,
        "themes": ["city", "nature", "food", "culture", "spring"],
        "companions": ["couple", "family", "solo", "friends"],
        "best_seasons": ["spring (September-November)", "autumn (March-May)"],
        "seasonal_highlights": {
            "spring": "Royal Botanic Gardens in bloom, Tesselaar Tulip Festival (Sep-Oct), Spring Racing Carnival (Oct-Nov)",
            "autumn": "Mild weather, wine harvest in Yarra Valley",
        },
        "activities": [
            {
                "name": "Royal Botanic Gardens spring bloom walk",
                "price_idr": 0,
                "duration_hours": 3,
                "tags": ["spring", "nature", "free", "family"],
            },
            {
                "name": "Tesselaar Tulip Festival (Sep-Oct)",
                "price_idr": 320000,
                "duration_hours": 4,
                "tags": ["spring", "nature", "photo", "family"],
            },
            {
                "name": "Great Ocean Road & Twelve Apostles day tour",
                "price_idr": 1300000,
                "duration_hours": 12,
                "tags": ["nature", "photo", "couple"],
            },
            {
                "name": "Laneway street art & coffee culture walk",
                "price_idr": 150000,
                "duration_hours": 3,
                "tags": ["city", "culture", "budget", "solo"],
            },
            {
                "name": "Queen Victoria Market food tour",
                "price_idr": 400000,
                "duration_hours": 3,
                "tags": ["food", "local", "family"],
            },
            {
                "name": "Phillip Island penguin parade",
                "price_idr": 900000,
                "duration_hours": 8,
                "tags": ["nature", "wildlife", "family"],
            },
            {
                "name": "Yarra Valley winery day (spring vineyards)",
                "price_idr": 1400000,
                "duration_hours": 8,
                "tags": ["spring", "food", "couple", "luxury"],
            },
            {
                "name": "MCG sports tour / Australian Open precinct",
                "price_idr": 350000,
                "duration_hours": 3,
                "tags": ["city", "sports"],
            },
        ],
        "hotels": [
            {
                "name": "CBD backpacker hostel",
                "tier": "budget",
                "price_idr_per_night": 550000,
                "tags": ["budget", "solo"],
            },
            {
                "name": "Southbank 4-star riverside hotel",
                "tier": "mid",
                "price_idr_per_night": 2100000,
                "tags": ["couple", "family"],
            },
            {
                "name": "Crown Towers Melbourne",
                "tier": "luxury",
                "price_idr_per_night": 5500000,
                "tags": ["luxury", "city_view"],
            },
        ],
        "daily_food_cost_idr": {"budget": 350000, "mid": 700000, "luxury": 1800000},
        "local_transport_cost_idr_per_day": 120000,
    },
    "paris": {
        "name": "Paris",
        "country": "France",
        "region": "Europe",
        "domestic_for_indonesia": False,
        "themes": ["culture", "city", "romantic", "history", "food", "luxury"],
        "companions": ["couple", "solo", "family", "friends"],
        "best_seasons": ["spring (April-June)", "autumn (September-October)"],
        "seasonal_highlights": {
            "spring": "Gardens in bloom at Luxembourg and Tuileries, cafe terraces open",
            "autumn": "Golden foliage along the Seine, fewer crowds",
        },
        "activities": [
            {
                "name": "Louvre Museum (timed entry)",
                "price_idr": 380000,
                "duration_hours": 4,
                "tags": ["culture", "history"],
            },
            {
                "name": "Eiffel Tower summit",
                "price_idr": 480000,
                "duration_hours": 3,
                "tags": ["city", "romantic", "photo"],
            },
            {
                "name": "Seine river evening cruise",
                "price_idr": 280000,
                "duration_hours": 2,
                "tags": ["romantic", "couple"],
            },
            {
                "name": "Montmartre & Sacre-Coeur walk",
                "price_idr": 0,
                "duration_hours": 3,
                "tags": ["culture", "free", "photo"],
            },
            {
                "name": "Versailles Palace half-day trip",
                "price_idr": 550000,
                "duration_hours": 6,
                "tags": ["history", "culture"],
            },
            {
                "name": "Patisserie & fromagerie tasting walk",
                "price_idr": 650000,
                "duration_hours": 3,
                "tags": ["food", "local", "couple"],
            },
            {
                "name": "Michelin-starred dinner",
                "price_idr": 3500000,
                "duration_hours": 3,
                "tags": ["luxury", "food", "romantic"],
            },
        ],
        "hotels": [
            {
                "name": "Montmartre budget hotel",
                "tier": "budget",
                "price_idr_per_night": 1500000,
                "tags": ["budget", "solo"],
            },
            {
                "name": "Le Marais boutique 4-star",
                "tier": "mid",
                "price_idr_per_night": 3500000,
                "tags": ["couple", "romantic"],
            },
            {
                "name": "Palace hotel on Place Vendome",
                "tier": "luxury",
                "price_idr_per_night": 15000000,
                "tags": ["luxury", "iconic"],
            },
        ],
        "daily_food_cost_idr": {"budget": 500000, "mid": 1000000, "luxury": 3000000},
        "local_transport_cost_idr_per_day": 180000,
    },
    "rome": {
        "name": "Rome",
        "country": "Italy",
        "region": "Europe",
        "domestic_for_indonesia": False,
        "themes": ["culture", "history", "food", "romantic", "city"],
        "companions": ["couple", "solo", "family", "friends"],
        "best_seasons": ["spring (April-May)", "autumn (September-October)"],
        "seasonal_highlights": {
            "spring": "Azaleas on the Spanish Steps, pleasant walking weather",
            "autumn": "Harvest cuisine season, thinner crowds at ruins",
        },
        "activities": [
            {
                "name": "Colosseum + Roman Forum combined entry",
                "price_idr": 320000,
                "duration_hours": 4,
                "tags": ["history", "culture"],
            },
            {
                "name": "Vatican Museums & Sistine Chapel",
                "price_idr": 350000,
                "duration_hours": 4,
                "tags": ["culture", "history"],
            },
            {
                "name": "Trevi Fountain & Pantheon evening walk",
                "price_idr": 0,
                "duration_hours": 2,
                "tags": ["romantic", "free", "photo"],
            },
            {
                "name": "Trastevere food tour (pasta + gelato)",
                "price_idr": 700000,
                "duration_hours": 3,
                "tags": ["food", "local", "couple"],
            },
            {
                "name": "Pasta-making class with market visit",
                "price_idr": 900000,
                "duration_hours": 4,
                "tags": ["food", "family", "culture"],
            },
            {
                "name": "Borghese Gallery & gardens",
                "price_idr": 250000,
                "duration_hours": 3,
                "tags": ["culture", "nature"],
            },
        ],
        "hotels": [
            {
                "name": "Termini district guesthouse",
                "tier": "budget",
                "price_idr_per_night": 1300000,
                "tags": ["budget", "solo"],
            },
            {
                "name": "Centro Storico 4-star",
                "tier": "mid",
                "price_idr_per_night": 3000000,
                "tags": ["couple", "family"],
            },
            {
                "name": "Rooftop luxury hotel near Spanish Steps",
                "tier": "luxury",
                "price_idr_per_night": 12000000,
                "tags": ["luxury", "romantic"],
            },
        ],
        "daily_food_cost_idr": {"budget": 450000, "mid": 900000, "luxury": 2500000},
        "local_transport_cost_idr_per_day": 150000,
    },
}

DESTINATION_ALIASES: dict[str, str] = {
    "korea": "seoul",
    "south korea": "seoul",
    "seoul": "seoul",
    "japan": "tokyo_kyoto",
    "tokyo": "tokyo_kyoto",
    "kyoto": "tokyo_kyoto",
    "bali": "bali",
    "indonesia": "bali",
    "labuan bajo": "labuan_bajo",
    "labuan": "labuan_bajo",
    "komodo": "labuan_bajo",
    "flores": "labuan_bajo",
    "singapore": "singapore",
    "melbourne": "melbourne",
    "australia": "melbourne",
    "paris": "paris",
    "france": "paris",
    "rome": "rome",
    "italy": "rome",
}

EUROPE_KEYS = ("paris", "rome")


def _summary(key: str, entry: dict) -> dict:
    return {
        "destination_key": key,
        "name": entry["name"],
        "country": entry["country"],
        "region": entry["region"],
        "domestic_for_indonesia": entry["domestic_for_indonesia"],
        "themes": entry["themes"],
        "companions": entry["companions"],
        "best_seasons": entry["best_seasons"],
    }


def search_destinations(
    theme: str, season: str, companion: str, tool_context: ToolContext
) -> dict:
    """Search the curated destination catalog by theme, season, and travel companion.

    Use this tool to recommend destinations when the traveler has NOT specified
    one, or to find destinations matching a vibe such as "sakura", "spring",
    "beach", "luxury", "budget", "romantic", or "family".

    Args:
        theme (str): Desired theme (e.g., "sakura", "beach", "culture", "luxury",
            "budget", "romantic"). Pass "any" for no theme filter.
        season (str): Desired travel season (e.g., "spring", "autumn"). Pass
            "any" for no season filter.
        companion (str): Travel party (e.g., "couple", "family", "solo",
            "friends"). Pass "any" for no companion filter.

    Returns:
        dict: {
            "status": "success",
            "destinations": [summary dicts with name, country, themes, seasons],
            "count": int,
            "data_source": "curated_catalog"
        }
    """
    theme_q = theme.strip().lower()
    season_q = season.strip().lower()
    companion_q = companion.strip().lower()

    def matches(entry: dict) -> bool:
        if theme_q not in ("", "any") and theme_q not in entry["themes"]:
            return False
        if season_q not in ("", "any"):
            seasons_text = " ".join(entry["best_seasons"]).lower()
            highlights_text = " ".join(entry["seasonal_highlights"].values()).lower()
            if season_q not in seasons_text and season_q not in highlights_text:
                return False
        if companion_q not in ("", "any") and companion_q not in entry["companions"]:
            return False
        return True

    results = [
        _summary(key, entry)
        for key, entry in DESTINATION_CATALOG.items()
        if matches(entry)
    ]
    return {
        "status": "success",
        "destinations": results,
        "count": len(results),
        "data_source": "curated_catalog",
    }


def get_destination_guide(destination: str, tool_context: ToolContext) -> dict:
    """Get the full itinerary-building guide for a destination.

    Use this tool once a destination is known. It returns activities with IDR
    prices and durations, hotels across budget/mid/luxury tiers with nightly
    rates, daily food and transport cost estimates, and seasonal highlights.
    Use these prices to build per-activity, per-day, and trip-total cost
    breakdowns.

    Args:
        destination (str): Destination name, country, or region (e.g., "Bali",
            "Korea", "Japan", "Labuan Bajo", "Singapore", "Melbourne",
            "Europe").

    Returns:
        dict: {
            "status": "success",
            "guides": [full catalog entries with activities, hotels, costs],
            "data_source": "curated_catalog"
        }
        For "Europe", multiple city guides are returned so a multi-city
        itinerary can be composed. On unknown destinations, returns
        status "not_found" with the list of available destinations.
    """
    query = destination.strip().lower()

    if "europe" in query:
        keys = list(EUROPE_KEYS)
    else:
        matched = DESTINATION_ALIASES.get(query)
        if matched is None:
            matched = next(
                (
                    mapped
                    for alias, mapped in DESTINATION_ALIASES.items()
                    if alias in query
                ),
                None,
            )
        keys = [matched] if matched else []

    if not keys:
        return {
            "status": "not_found",
            "error_message": f"No curated guide for '{destination}'.",
            "available_destinations": sorted(
                {entry["name"] for entry in DESTINATION_CATALOG.values()}
            ),
            "note": "Build the itinerary from general knowledge but state that prices are estimates, or suggest a catalog destination.",
        }

    guides = [{"destination_key": key, **DESTINATION_CATALOG[key]} for key in keys]
    return {
        "status": "success",
        "guides": guides,
        "count": len(guides),
        "data_source": "curated_catalog",
    }

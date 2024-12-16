import pandas as pd
import numpy as np
from geopy.distance import geodesic
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Reference points for calculating area appeal
reference_points = {
    "city_center": {"coords": (43.2220, 76.8512), "weight": 0.3},
    "airport": {"coords": (43.3521, 77.0405), "weight": 0.15},
    "presidents_park": {"coords": (43.1983, 76.8800), "weight": 0.1},
    "dostyk_plaza": {"coords": (43.2380, 76.9582), "weight": 0.15},
    "kok_tobe": {"coords": (43.2312, 76.9597), "weight": 0.1},
    "mega_park_mall": {"coords": (43.2622, 76.9264), "weight": 0.1},
    "shymbulak_ski_resort": {"coords": (43.1590, 77.0815), "weight": 0.05},
    "almaty_tower": {"coords": (43.2389, 76.9124), "weight": 0.1},
    "esentai_mall": {"coords": (43.2236, 76.9266), "weight": 0.1},
    "central_park": {"coords": (43.2545, 76.9515), "weight": 0.05},
    "raiymbek_batyr": {"coords": (43.2709, 76.9422), "weight": 0.1},
    "zhibek_zholy": {"coords": (43.2582, 76.9465), "weight": 0.1},
    "almaly": {"coords": (43.2522, 76.9476), "weight": 0.1},
    "abay": {"coords": (43.2451, 76.9479), "weight": 0.1},
    "baikonur": {"coords": (43.2332, 76.9496), "weight": 0.1},
    "auezov_theater": {"coords": (43.2277, 76.9501), "weight": 0.1},
    "alatau": {"coords": (43.2178, 76.9439), "weight": 0.1},
    "sairan": {"coords": (43.2106, 76.9247), "weight": 0.1},
    "moscow": {"coords": (43.2074, 76.9038), "weight": 0.1},
    "sayahat": {"coords": (43.2561, 76.9101), "weight": 0.1},
    "railway_station_1": {"coords": (43.2567, 76.9278), "weight": 0.05},
    "railway_station_2": {"coords": (43.2615, 76.9214), "weight": 0.05}
}

def preprocess_input(data):
    """Preprocess input data for prediction."""
    try:
        unnecessary_columns = ["id", "title", "street", "house_num", "is_pledged", "was_former_hostel", "country", "city", "microdistrict"]
        data = data.drop(columns=unnecessary_columns, errors='ignore')

        columns_to_drop = ["price", "balcony", "bathroom", "furniture_status", "security"]
        data = data.drop(columns=columns_to_drop, errors='ignore')

        pd.set_option('future.no_silent_downcasting', True)
        data.replace([None], np.nan, inplace=True)

        # Feature engineering with floor
        data['middle_floor'] = data['total_floors'] / 2
        data['floor_ratio'] = 1 - (abs(data['floor'] - data['middle_floor']) / (data['total_floors'] / 2))
        data = data.drop(columns=['floor', 'middle_floor'], errors='ignore')

        # Feature engineering with geo data (lon, lat)
        def calculate_area_appeal(row):
            appeal_score = 0
            for point_name, details in reference_points.items():
                coords = details["coords"]
                weight = details["weight"]
                distance = geodesic((row['lat'], row['lon']), coords).km
                appeal_score += weight * (1 / (distance + 1))
            return appeal_score

        data['area_appeal'] = data.apply(calculate_area_appeal, axis=1)
        data = data.drop(columns=['lat', 'lon'], errors='ignore')

        if data.isnull().any().any():
            raise ValueError(f"The following columns contain null values after preprocessing: {data.columns[data.isnull().any()].tolist()}")

        return data
    except Exception as e:
        logger.error(f"Error during preprocessing: {e}")
        raise e

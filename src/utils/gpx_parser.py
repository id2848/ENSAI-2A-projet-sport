import gpxpy

def parse_gpx(content):
    gpx = gpxpy.parse(content)

    # Métadonnées de base
    name = gpx.tracks[0].name if gpx.tracks[0] else "Mon activité"
    sport = gpx.tracks[0].type if gpx.tracks[0] else ""
    date_str = gpx.time.strftime("%Y-%m-%d")

    # Stats de base
    distance_m = gpx.length_3d()                    # mètres
    duration_s = gpx.get_duration()                 # secondes
    moving = gpx.get_moving_data()                  # temps/distance/vitesse en mouvement
    moving_time_s = moving.moving_time
    moving_distance_m = moving.moving_distance
    moving_max_speed_ms = moving.max_speed

    # Métriques calculées
    distance_km = distance_m / 1000
    duration_min = duration_s / 60
    duration_h = duration_s / 3600
    avg_speed_kmh = distance_km / duration_h
    moving_distance_km = moving_distance_m/1000
    moving_time_min = moving_time_s/60
    moving_max_speed_kmh = moving_max_speed_ms*3.6
    moving_speed_kmh = (
        (moving_distance_m / 1000) / (moving_time_s / 3600)
        if moving and moving_time_s > 0 else 0
    )

    return {
        "nom": name,
        "type": sport,
        "date": date_str,                                       # date
        "distance totale": round(distance_km, 3),               # km
        "durée totale": round(duration_min, 2),                 # min
        "vitesse moyenne": round(avg_speed_kmh, 2),             # km/h
        "vitesse max": round(moving_max_speed_kmh, 2),          # km/h
        "distance en mvt": round(moving_distance_km, 3),        # km
        "temps en mvt": round(moving_time_min, 2),              # min
        "vitesse moyenne en mvt": round(moving_speed_kmh, 2),   # km/h
    }

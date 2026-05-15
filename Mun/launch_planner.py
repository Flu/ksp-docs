import math

EPOCH_KERBIN_MEAN_ANOMALY = 3.14 # radians
EPOCH_MUN_MEAN_ANOMALY = 1.7 # radians
KERBIN_LAN = 0.0
MUN_LAN = 0.0
KERBIN_ARG_PE = 0.0
MUN_ARG_PE = 0.0

KERBIN_ORBITAL_PERIOD = 9_203_544.6 # seconds
KERBIN_ANG_VELOCITY = 2*math.pi/KERBIN_ORBITAL_PERIOD

MUN_ORBITAL_PERIOD = 138_984.4 # seconds
MUN_ANG_VELOCITY = 2*math.pi/MUN_ORBITAL_PERIOD

KERBIN_DISTANCE = 13_599_840_256
MUN_DISTANCE = 12_000_000

def get_mun_tl_at(ut: float):
    epoch_tl = EPOCH_MUN_MEAN_ANOMALY + MUN_ARG_PE + MUN_LAN
    return epoch_tl + ut*MUN_ANG_VELOCITY

def get_kerbin_tl_at(ut: float):
    epoch_tl = EPOCH_KERBIN_MEAN_ANOMALY + KERBIN_ARG_PE + KERBIN_LAN
    return epoch_tl + ut*KERBIN_ANG_VELOCITY

def from_date_to_ut(year: int= 0, day: int = 0, hour: int = 0, minute: int = 0, second: int = 0) -> float:
    return (year-1)*KERBIN_ORBITAL_PERIOD + (day-1)*21_600 + hour*3600 + minute*60 + second

def from_ut_to_date(ut: float) -> tuple[int, int, int, int, float]:
    if ut <= 0:
        raise FloatingPointError
    
    years = math.floor(ut / KERBIN_ORBITAL_PERIOD)
    cut = ut % KERBIN_ORBITAL_PERIOD

    days = math.floor(cut / 21_600)
    cut %= 21_600

    hours = math.floor(cut / 3600)
    cut %= 3600

    minutes = math.floor(cut / 60)
    cut %= 60
    
    return (years + 1, days + 1, hours, minutes, cut)

def format_date(date):
    return f"Year {date[0]}, day {date[1]}, {date[2]}:{date[3]}:{int(date[4])}"

def get_mun_vector_at(ut: float):
    tl = get_mun_tl_at(ut)
    x = MUN_DISTANCE*math.cos(tl)
    y = MUN_DISTANCE*math.sin(tl)
    return (x, y)

def get_kerbin_vector_at(ut: float):
    tl = get_kerbin_tl_at(ut)
    x = KERBIN_DISTANCE*math.cos(tl)
    y = KERBIN_DISTANCE*math.sin(tl)
    return (x, y)

def add(vec1, vec2):
    return (vec1[0] + vec2[0], vec1[1] + vec2[1])

def to_polar(vec):
    r = math.sqrt(vec[0]**2 + vec[1]**2)
    theta = math.atan2(vec[1], vec[0])
    return r, theta

def find_eclipses(ut_time_start: int, ut_time_end: int):
    for time_ut in range(ut_time_start, ut_time_end):
        mun_pos = get_mun_vector_at(time_ut)
        kerbin_pos = get_kerbin_vector_at(time_ut)
        true_mun_pos = add(kerbin_pos, mun_pos)

        mun_polar = to_polar(true_mun_pos)
        kerbin_polar = to_polar(kerbin_pos)
        if abs(mun_polar[1] - kerbin_polar[1]) < 0.00000001 and mun_polar[0] < kerbin_polar[0]:
            print(format_date(from_ut_to_date(time_ut)))
            
def main():
    find_eclipses(ut_time_start=int(from_date_to_ut(year=1)), ut_time_end=int(from_date_to_ut(year=3)))

if __name__ == "__main__":
    main()

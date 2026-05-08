import krpc
import time
import math

def run_dashboard():
    try:
        conn = krpc.connect(name='Dashboard')
    except ConnectionRefusedError:
        print("Error: Could not connect to KSP.")
        return

    vessel = conn.space_center.active_vessel
    mun = conn.space_center.bodies['Mun']

    ut = conn.add_stream(getattr, conn.space_center, 'ut')
    
    # Vessel streams
    v_alt = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
    v_speed = conn.add_stream(getattr, vessel.orbit, 'speed')
    v_fuel = conn.add_stream(vessel.resources.amount, 'LiquidFuel')
    v_true_anom = conn.add_stream(getattr, vessel.orbit, 'true_anomaly')

    # Mun streams
    m_speed = conn.add_stream(getattr, mun.orbit, 'speed')
    m_alt = conn.add_stream(getattr, mun.orbit, 'radius') # Radius is distance to center
    m_lan = conn.add_stream(getattr, mun.orbit, 'longitude_of_ascending_node')
    m_arg_pe = conn.add_stream(getattr, mun.orbit, 'argument_of_periapsis')
    m_true_anom = conn.add_stream(getattr, mun.orbit, 'true_anomaly')
    
    try:
        while True:
            # Clear screen/Move cursor to top
            print("\033[H\033[J", end="")
            
            print(f"UT: {ut():.2f}")
            print("\n== SHIP ==")
            print(f"{'Velocity':<15} {v_speed():>15.2f} m/s")
            print(f"{'Altitude':<15} {v_alt():>15.2f} m")
            print(f"{'Fuel':<15} {v_fuel():>15.2f} units")
            print(f"{'True Anom':<15} {math.degrees(v_true_anom()):>15.2f}°")

            print("\n== MUN ==")
            print(f"{'Velocity':<15} {m_speed():>15.2f} m/s")
            print(f"{'Distance':<15} {m_alt():>15.2f} m")
            print(f"{'LAN':<15} {math.degrees(m_lan()):>15.2f}°")
            print(f"{'Arg PE':<15} {math.degrees(m_arg_pe()):>15.2f}°")
            print(f"{'True Anom':<15} {math.degrees(m_true_anom()):>15.2f}°")
            
            time.sleep(0.13)
    except KeyboardInterrupt:
        print("\nDashboard closed.")

if __name__ == "__main__":
    run_dashboard()

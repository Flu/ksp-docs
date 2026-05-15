import krpc
import time
import math

class ShipTelemetry:
    def __init__(self, conn):
        self.vessel = conn.space_center.active_vessel
        self.ut = conn.add_stream(getattr, conn.space_center, 'ut')
        
        # Orbital parameters
        self.altitude = conn.add_stream(getattr, self.vessel.flight(), 'mean_altitude')
        self.orbital_speed = conn.add_stream(getattr, self.vessel.orbit, 'speed')
        self.mean_anomaly = conn.add_stream(getattr, self.vessel.orbit, 'mean_anomaly')
        self.eccentric_anomaly = conn.add_stream(getattr, self.vessel.orbit, 'eccentric_anomaly')
        self.true_anomaly = conn.add_stream(getattr, self.vessel.orbit, 'true_anomaly')
        self.arg_pe = conn.add_stream(getattr, self.vessel.orbit, 'argument_of_periapsis')
        self.lan = conn.add_stream(getattr, self.vessel.orbit, 'longitude_of_ascending_node')

        # Rotation
        self.rotation = conn.add_stream(getattr, self.vessel.flight(), 'rotation')
        
        # Resources
        self.fuel = conn.add_stream(self.vessel.resources.amount, 'LiquidFuel')
        self.oxidizer = conn.add_stream(self.vessel.resources.amount, 'Oxidizer')
        self.electric_charge = conn.add_stream(self.vessel.resources.amount, 'ElectricCharge')
        self.monopropellant = conn.add_stream(self.vessel.resources.amount, 'Monopropellant')

    def true_longitude(self):
        return (self.lan() + self.arg_pe() + self.true_anomaly()) % (2*math.pi)

class BodyTelemetry:
    def __init__(self, conn, name):
        self.name = name
        self.orbit = conn.space_center.bodies[name].orbit

        self.speed = conn.add_stream(getattr, self.orbit, 'speed')
        self.alt = conn.add_stream(getattr, self.orbit, 'radius')
        self.lan = conn.add_stream(getattr, self.orbit, 'longitude_of_ascending_node')
        self.arg_pe = conn.add_stream(getattr, self.orbit, 'argument_of_periapsis')
        self.true_anomaly = conn.add_stream(getattr, self.orbit, 'true_anomaly')

    def true_longitude(self):
        return (self.lan() + self.arg_pe() + self.true_anomaly()) % (2*math.pi)

def run_dashboard():
    try:
        conn = krpc.connect(name='Dashboard')
    except ConnectionRefusedError:
        print("Could not connect to KSP")
        return

    ship = ShipTelemetry(conn)
    mun = BodyTelemetry(conn, name='Mun')

    try:
        with open ("ascent_log.csv", "w") as output_file:
            output_file.write("UT,Altitude,OrbitalSpeed,TrueAnom,EccAnomaly,MeanAnomaly,TrueLong\n")
            while True:
                print("\033[H\033[J", end="")
            
                print(f"UT: {ship.ut():.2f}")
                print("\n== SHIP ==")
                print(f"{'Velocity':<15} {ship.orbital_speed():>15.2f} m/s")
                print(f"{'Altitude':<15} {ship.altitude():>15.2f} m")
                print(f"{'Fuel':<15} {ship.fuel():>15.2f} units")
                print(f"{'True Anom':<15} {math.degrees(ship.true_anomaly()):>15.2f}°")
                print(f"{'Ecc Anom':<15} {math.degrees(ship.eccentric_anomaly()):>15.2f}°")
                print(f"{'Mean Anom':<15} {math.degrees(ship.mean_anomaly()):>15.2f}°")
                print(f"{'True Long':<15} {math.degrees(ship.true_longitude()):>15.2f}°")

                output_file.write(f"{ship.ut():.2f},")
                output_file.write(f"{math.degrees(ship.altitude()):.3f},")
                output_file.write(f"{math.degrees(ship.orbital_speed()):.3f},")
                output_file.write(f"{math.degrees(ship.true_anomaly()):.3f},")
                output_file.write(f"{math.degrees(ship.eccentric_anomaly()):.3f},")
                output_file.write(f"{math.degrees(ship.mean_anomaly()):.3f},")
                output_file.write(f"{math.degrees(ship.true_longitude()):.3f}\n")
                
                print("\n== MUN ==")
                print(f"{'Velocity':<15} {mun.speed():>15.2f} m/s")
                print(f"{'Distance':<15} {mun.alt():>15.2f} m")
                print(f"{'LAN':<15} {math.degrees(mun.lan()):>15.2f}°")
                print(f"{'Arg PE':<15} {math.degrees(mun.arg_pe()):>15.2f}°")
                print(f"{'True Anom':<15} {math.degrees(mun.true_anomaly()):>15.2f}°")
                print(f"{'True Long':<15} {math.degrees(mun.true_longitude()):>15.2f}°")
                
                time.sleep(0.2)
            
    except KeyboardInterrupt:
        print("Keyboard interrupt on the dashboard caught. Exiting.")
    except:
        print("Unknown error occurred. Exiting.")
    finally:
        return

if __name__ == "__main__":
    run_dashboard()

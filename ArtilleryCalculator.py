import math

def main():
    print("Firing angle and distance calculator (Roblox-style).")
    print("• Gravity (g) = 17 studs/s^2")
    print("• Enter A, B as float values (number of squares).")
    print("• Then enter height state: -1 (lower), 0 (same level), 1 (higher).")
    print("• Then enter cover state: 0 (not behind building), 1 (behind building => +2.5°).")
    print("• If range > 2500 studs, it's impossible to hit.\n")
    print("Commands in input:")
    print("  'C'  => change square size (studs)")
    print("  'CE' => change projectile speed (studs/s)")
    print("  'q'  => quit\n")

    g = 17.0         # gravity in studs/s^2
    EPS = 1e-7       # small epsilon for clamping sin(2θ)
    DECIMALS = 2     # how many decimals to show
    MAX_RANGE = 2500 # if distance > 2500 studs => impossible to hit

    def set_square_size():
        """Ask user for the square size in studs."""
        while True:
            try:
                size = float(input("Enter the square size (studs): "))
                if size <= 0:
                    print("Square size must be > 0.")
                    continue
                return size
            except ValueError:
                print("Error: please enter a numeric value (integer or float).")

    def set_projectile_speed():
        """Ask user for the projectile speed in studs/s."""
        while True:
            try:
                speed = float(input("Enter the projectile speed (studs/s): "))
                if speed <= 0:
                    print("Speed must be > 0.")
                    continue
                return speed
            except ValueError:
                print("Error: please enter a numeric value (integer or float).")

    # Initial setup
    square_size = set_square_size()
    projectile_speed = set_projectile_speed()

    print(f"\nCurrent parameters:")
    print(f"  - Square size: {square_size} studs")
    print(f"  - Projectile speed: {projectile_speed} studs/s")
    print(f"  - Gravity: {g} studs/s^2\n")

    while True:
        try:
            # Input A
            a_input = input("Enter A (number of squares along axis A): ").strip().lower()
            if a_input == 'q':
                print("Quitting. Goodbye!")
                break
            elif a_input == 'c':
                square_size = set_square_size()
                print(f"New square size: {square_size} studs.\n")
                continue
            elif a_input == 'ce':
                projectile_speed = set_projectile_speed()
                print(f"New projectile speed: {projectile_speed} studs/s.\n")
                continue

            A = float(a_input)
            if A < 0:
                print("A must be >= 0. Try again.\n")
                continue

            # Input B
            b_input = input("Enter B (number of squares along axis B): ").strip().lower()
            if b_input == 'q':
                print("Quitting. Goodbye!")
                break
            elif b_input == 'c':
                square_size = set_square_size()
                print(f"New square size: {square_size} studs.\n")
                continue
            elif b_input == 'ce':
                projectile_speed = set_projectile_speed()
                print(f"New projectile speed: {projectile_speed} studs/s.\n")
                continue

            B = float(b_input)
            if B < 0:
                print("B must be >= 0. Try again.\n")
                continue

            # Input height state
            h_input = input("Enter height state (-1 lower, 0 same, 1 higher): ").strip()
            try:
                height_state = int(h_input)
                if height_state not in [-1, 0, 1]:
                    print("Height state must be -1, 0, or 1.\n")
                    continue
            except ValueError:
                print("Error: enter -1, 0, or 1.\n")
                continue

            # Input cover state
            cover_input = input("Is the target behind a building? (1 => +2.5°, 0 => no): ").strip()
            try:
                cover_state = int(cover_input)
                if cover_state not in [0, 1]:
                    print("Error: enter 0 or 1.\n")
                    continue
            except ValueError:
                print("Error: enter 0 or 1.\n")
                continue

            # Calculate distance
            distance = math.sqrt((A * square_size)**2 + (B * square_size)**2)
            print(f"\nHorizontal distance to target: {distance:.{DECIMALS}f} studs")

            # Check max range
            if distance > MAX_RANGE:
                print("Impossible to hit (distance > 2500 studs).")
                continue

            if distance == 0:
                print("Distance = 0. No angle needed.\n")
                continue

            # sin(2θ) = (distance*g)/(v^2)
            ratio = (distance * g) / (projectile_speed**2)

            # Soft clamping
            if ratio > 1.0:
                if ratio <= 1.0 + EPS:
                    ratio = 0.9999999
                else:
                    print("Impossible to hit (sin(2θ) > 1). Increase speed.\n")
                    continue
            elif ratio < 0:
                if ratio >= -EPS:
                    ratio = 0.0
                else:
                    print("Impossible to hit (sin(2θ) < 0). Check inputs.\n")
                    continue

            ratio = max(0.0, min(1.0, ratio))

            angle_rad = 0.5 * math.asin(ratio)
            angle_deg = math.degrees(angle_rad)

            # Height adjustment
            if height_state == -1:
                angle_deg -= 0.5
            elif height_state == 1:
                angle_deg += 1.0

            # Cover adjustment
            if cover_state == 1:
                angle_deg += 2.5

            print(f"Recommended low angle: {angle_deg:.{DECIMALS}f}°\n")

        except ValueError:
            print("Error: enter numeric values, or 'C'/'CE'/'q' as commands.\n")
        except ZeroDivisionError:
            print("Error: division by zero. Check projectile speed.\n")
        except Exception as e:
            print(f"Unexpected error: {e}\n")

if __name__ == "__main__":
    main()

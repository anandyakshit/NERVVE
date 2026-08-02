import serial
import re

PORT = "COM3"       # Change this
BAUD = 115200

TOTAL_PACKETS = 51  # TEST|0 to TEST|50

received = set()

rssi_values = []
snr_values = []

ser = serial.Serial(PORT, BAUD, timeout=1)

print("Listening for packets...\n")

current_test = None


while True:

    try:
        line = ser.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()


        if not line:
            continue


        print(line)


        # Capture TEST number
        test_match = re.match(r"TEST\|(\d+)", line)

        if test_match:

            current_test = int(test_match.group(1))

            if 0 <= current_test <= 50:

                received.add(current_test)



        # Capture RSSI
        rssi_match = re.match(r"RSSI:(-?\d+)", line)

        if rssi_match:

            rssi = int(rssi_match.group(1))

            rssi_values.append(rssi)



        # Capture SNR
        snr_match = re.match(r"SNR:(-?\d+\.\d+)", line)

        if snr_match:

            snr = float(snr_match.group(1))

            snr_values.append(snr)



        # Finished test
        if len(received) == TOTAL_PACKETS:


            print("\n==============================")
            print("       TEST COMPLETE")
            print("==============================")

            missing = [
                x for x in range(51)
                if x not in received
            ]


            print(
                f"Packets Received: "
                f"{len(received)}/{TOTAL_PACKETS}"
            )

            print(
                f"Packet Loss: "
                f"{(1-len(received)/TOTAL_PACKETS)*100:.2f}%"
            )


            if rssi_values:

                print("\nRSSI Statistics")

                print(
                    f"Average: {sum(rssi_values)/len(rssi_values):.2f} dBm"
                )

                print(
                    f"Minimum: {min(rssi_values)} dBm"
                )

                print(
                    f"Maximum: {max(rssi_values)} dBm"
                )


            if snr_values:

                print("\nSNR Statistics")

                print(
                    f"Average: {sum(snr_values)/len(snr_values):.2f} dB"
                )

                print(
                    f"Minimum: {min(snr_values):.2f} dB"
                )

                print(
                    f"Maximum: {max(snr_values):.2f} dB"
                )


            print("\nMissing Packets:")
            print(missing)

            print("==============================")

            break



    except KeyboardInterrupt:

        print("\nStopped")

        break



ser.close()

import time
import pyvisa

def calculate_resistance(inst, current):
    """
    Reads the voltage from the oscilloscope and calculates resistance using Ohm's Law.
    
    :param inst: VISA instrument object (oscilloscope)
    :param current: Measured current in amperes (A)
    :return: Calculated resistance in ohms (Ω)
    """
    try:
        if current == 0:
            raise ValueError("Current cannot be zero to avoid division by zero.")

        # 1) Set measurement to Mean Voltage (DC Average)
        inst.write("PACU MEAN,C1")
        time.sleep(1)

        # 2) Query the oscilloscope for the voltage
        voltage_mean = inst.query("C1:PAVA? MEAN").strip()

        # 3) Extract the numeric value from response
        try:
            voltage_value = float(voltage_mean.split(",")[1].replace("V", ""))
        except (IndexError, ValueError):
            raise ValueError(f"Unexpected voltage response: {voltage_mean}")

        # 4) Calculate Resistance (Ohm's Law: R = V / I)
        resistance = voltage_value / current
        print(f"Calculated Resistance: {resistance:.2f} Ω")

        return resistance

    except pyvisa.VisaIOError as e:
        print("VISA I/O Error:", e)
    except Exception as e:
        print("General Error:", e)

def check_communication(inst):
    try:
        # 1) Query *IDN?
        time.sleep(0.5)
        idn_response = inst.query("*IDN?")
        print("IDN Response:", repr(idn_response))

        # 2) Query *OPC? (Check operation complete)
        time.sleep(0.5)
        opc_response = inst.query("*OPC?")
        print("OPC Response:", repr(opc_response))

        # 3) Reset the instrument
        time.sleep(0.5)
        inst.write("*RST")
        time.sleep(2)  # Allow reset to complete

        # 4) Query *OPC? after reset
        opc_after_reset = inst.query("*OPC?")
        print("OPC after *RST:", repr(opc_after_reset))

    except pyvisa.VisaIOError as e:
        print("VISA I/O Error:", e)
    except Exception as e:
        print("General Error:", e)

def check_inr(inst):
    try:
        # Wait a moment to ensure INR register updates
        time.sleep(1)

        # Query INR? (Internal Register)
        inr_response = inst.query("INR?")
        print("INR Response:", repr(inr_response))

    except pyvisa.VisaIOError as e:
        print("VISA I/O Error:", e)
    except Exception as e:
        print("General Error:", e)

def continuous_dc_average(inst):
    try:
        inst.write("PACU MEAN,C1")  # Set DC Average Measurement

        while True:
            voltage_mean = inst.query("C1:PAVA? MEAN").strip()
            voltage_mean_mv = float(voltage_mean.split(",")[1].replace("V", "")) * 1000
            print(f"MEAN: {voltage_mean_mv:.2f} mV")
            time.sleep(0.1)  # Read every 1 second

    except KeyboardInterrupt:
        print("\nStopped by user.")

    except pyvisa.VisaIOError as e:
        print("VISA I/O Error:", e)
    except Exception as e:
        print("General Error:", e)

def continuous_measurement(inst):
    """
    Continuously measures BASE, RMS, MEAN, and AMPL on Channel 1 and 2.
    All values are converted to millivolts (mV).
    Calculate Sensor Resistance (Ω).
    Press Ctrl + C to stop the loop.
    """

    # Resistance(10 Ohm)
    R = 10.0

    try:
        # 1) Set up the measurements for BASE, RMS, MEAN, AMPL
        # inst.write("PACU BASE,C1")
        # inst.write("PACU AMPL,C1")
        inst.write("PACU RMS,C1")
        inst.write("PACU MEAN,C1")
        inst.write("PACU RMS,C2")
        inst.write("PACU MEAN,C2")

        while True:
            # 2) Query the oscilloscope for all four values
            # base = inst.query("C1:PAVA? BASE").strip()
            # ampl = inst.query("C1:PAVA? AMPL").strip()
            rms_c1 = inst.query("C1:PAVA? RMS").strip()
            mean_c1 = inst.query("C1:PAVA? MEAN").strip()
            rms_c2 = inst.query("C2:PAVA? RMS").strip()
            mean_c2 = inst.query("C2:PAVA? MEAN").strip()

            # 3) Extract numeric values and convert to millivolts
            try:
                # base_mv = float(base.split(",")[1].replace("V", "")) * 1000
                # ampl_mv = float(ampl.split(",")[1].replace("V", "")) * 1000
                rms_c1_mv = float(rms_c1.split(",")[1].replace("V", "")) * 1000
                mean_c1_mv = float(mean_c1.split(",")[1].replace("V", "")) * 1000
                rms_c2_mv = float(rms_c2.split(",")[1].replace("V", "")) * 1000
                mean_c2_mv = float(mean_c2.split(",")[1].replace("V", "")) * 1000

                r_sensor = (mean_c1_mv / mean_c2_mv) * R

            except (IndexError, ValueError):
                print(f"Unexpected response - RMS_C1: {rms_c1}, MEAN_C1: {mean_c1}, RMS_C2: {rms_c2}, MEAN_C2: {mean_c2}")
                continue  # Skip this iteration if parsing fails

            # 4) Print the results in mV
            print(f"RMS_C1: {rms_c1_mv:.2f} mV | MEAN_C1: {mean_c1_mv:.2f} mV | RMS_C2: {rms_c2_mv:.2f} mV | MEAN_C2: {mean_c2_mv:.2f} mV | R_SENSOR: {r_sensor:.2f} Ω")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopped by user.")
    except pyvisa.VisaIOError as e:
        print("VISA I/O Error:", e)
    except Exception as e:
        print("General Error:", e)

def main():
    rm = pyvisa.ResourceManager("@py")  # Use PyVISA-Py
    scope_address = "USB0::0x3121::0x2100::641G22175::INSTR"

    try:
        inst = rm.open_resource(scope_address)
        inst.timeout = 5000  # 10 seconds

        # check_communication(inst)
        continuous_measurement(inst)

    except pyvisa.VisaIOError as e:
        print("VISA I/O Error:", e)
    except Exception as e:
        print("General Error:", e)
    finally:
        inst.close()

if __name__ == "__main__":
    main()

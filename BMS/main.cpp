#include <stdio.h>
#include <math.h>

const float battery_nominal_capacity = 40.0;
const float system_nominal_voltage = 48.0;
const float minimum_required_power = 1500.0;
const float total_energy = system_nominal_voltage * battery_nominal_capacity;

float SOH = 1.0;
float SOC = 100.0;
float DOD = 0.0;
float Q_releasable = battery_nominal_capacity;

const float coulombic_efficiency_charge = 0.95;
const float coulombic_efficiency_discharge = 0.98;


const float voltage_SOC_map[] = {43.2, 45.6, 48.0, 50.4, 52.8};
const float SOC_levels[] = {0.0, 25.0, 50.0, 75.0, 100.0};

const float peukert_exponent = 1.1;

float capacity_at_c_rate(float c_rate, float voltage) {
    if (c_rate == 1.0 && voltage == 42) return 22.0;
    if (c_rate == 3.0 && voltage == 43.2) return 30.0;
    if (c_rate == 10.0 && voltage == 43.2) return 40.0;
    return battery_nominal_capacity;
}

float peukert_effect(float current, float capacity) {
    if (current <= 0) return capacity;
    return capacity / pow(fabs(current), (peukert_exponent - 1));
}

float calibrate_SOC(float voltage) {
    for (int i = 0; i < sizeof(voltage_SOC_map) / sizeof(voltage_SOC_map[0]) - 1; i++) {
        if (voltage >= voltage_SOC_map[i] && voltage <= voltage_SOC_map[i + 1]) {
            float soc = SOC_levels[i] + (SOC_levels[i + 1] - SOC_levels[i]) *
                        (voltage - voltage_SOC_map[i]) / (voltage_SOC_map[i + 1] - voltage_SOC_map[i]);
            return soc;
        }
    }
    return (voltage < voltage_SOC_map[0]) ? 0.0 : 100.0;
}

int main() {
    int n;
    float time_period;

    printf("Enter the number of voltage-current pairs: ");
    scanf("%d", &n);

    printf("Enter the time period (hours): ");
    scanf("%f", &time_period);

    float battery_voltage, current;

    float time_in_seconds = time_period * 3600.0;

    for (int i = 0; i < n; i++) {
        printf("Enter voltage (V) and current (A) for pair %d: ", i + 1);
        scanf("%f %f", &battery_voltage, &current);

        float c_rate = fabs(current) / battery_nominal_capacity;
        float adjusted_capacity = capacity_at_c_rate(c_rate, battery_voltage);

        adjusted_capacity = peukert_effect(current, adjusted_capacity);

        float delta_Q = 0.0;
        if (current > 0) {
            delta_Q = current * coulombic_efficiency_charge * (time_in_seconds / 3600.0);
        } else {
            delta_Q = current * coulombic_efficiency_discharge * (time_in_seconds / 3600.0);
        }

        Q_releasable -= delta_Q;

        if (Q_releasable > adjusted_capacity) Q_releasable = adjusted_capacity;
        if (Q_releasable < 0) Q_releasable = 0;

        DOD = 100.0 * (1 - Q_releasable / adjusted_capacity);
        SOC = 100.0 - DOD;

        if (fabs(current) < 0.1) {
            float SOC_OCV = calibrate_SOC(battery_voltage);
            float error = SOC_OCV - SOC;

            float correction_factor = 1.0 + (error / 100.0);
            SOC += error;

            Q_releasable = battery_nominal_capacity * SOC / 100.0;
        }

        if (SOC == 100.0 || SOC == 0.0) {
            SOH = (SOH * 0.99) + (Q_releasable / battery_nominal_capacity) * 0.01;
        }

        printf("Pair %d -> Voltage (V): %.2f | Current (A): %.2f | SOC (%%): %.2f | SOH (%%): %.2f\n",
               i + 1, battery_voltage, current, SOC, SOH * 100.0);

        float remaining_energy = SOC / 100.0 * total_energy;
        if (remaining_energy < minimum_required_power) {
            printf("Critical Warning: System energy below 1500 Wh! Immediate action required.\n");
        }

        if (SOC <= 50.0 && SOC > 20.0) {
            printf("Warning: Battery SOC has reached 50%%! Please Go to the nearest charging station.\n");
        }

        if (SOC <= 20.0) {
            printf("Warning: Battery SOC has reached 20%%! Please stop for recharge the battery immediately.\n");
        }
    }

    return 0;
}

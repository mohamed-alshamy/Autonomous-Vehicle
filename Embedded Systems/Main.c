/*
 * Main.c
 *
 *  Created on: 23 Nov 2024
 *      Author: EN . MAHMOUD TAMER
 */
#include "Main.h"

void ultrasonic_init(void) {
    // TRIG pins outputs
    DDRC |= (1 << TRIG1) | (1 << TRIG2) | (1 << TRIG3) | (1 << TRIG4);

    // ECHO pins inputs
    DDRD &= ~((1 << ECHO1) | (1 << ECHO2) | (1 << ECHO3) | (1 << ECHO4));
    // Trig is Low
    PORTC &= ~((1 << TRIG1) | (1 << TRIG2) | (1 << TRIG3) | (1 << TRIG4));
}

uint16_t measure_distance(uint8_t trig_pin, uint8_t echo_pin) {
    uint16_t pulse_duration = 0;

    // Send trigger pulse
    PORTC |= (1 << trig_pin);
    _delay_us(10);
    PORTC &= ~(1 << trig_pin);


    while(!(PIND & (1 << echo_pin)));

    // Measure pulse duration
    while(PIND & (1 << echo_pin)) {
        pulse_duration++;
        _delay_us(1);
        if(pulse_duration > 23200) break; // Timeout after 4ms
    }


    return pulse_duration / 58;
}
uint16_t get_sensor1_distance(void) {
    return measure_distance(TRIG1, ECHO1);
}

uint16_t get_sensor2_distance(void) {
    return measure_distance(TRIG2, ECHO2);
}

uint16_t get_sensor3_distance(void) {
    return measure_distance(TRIG3, ECHO3);
}

uint16_t get_sensor4_distance(void) {
    return measure_distance(TRIG4, ECHO4);
}
int main(void) {

    uint16_t distance1, distance2, distance3, distance4;

    ultrasonic_init();

    // Enable interrupts
    sei();

    while(1) {
        // Get distances from 4 sensors
        distance1 = get_sensor1_distance();
        _delay_ms(50);

        distance2 = get_sensor2_distance();
        _delay_ms(50);

        distance3 = get_sensor3_distance();
        _delay_ms(50);

        distance4 = get_sensor4_distance();
        _delay_ms(50);

    }
    return 0;
}


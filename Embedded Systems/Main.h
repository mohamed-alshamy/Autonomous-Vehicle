/*
 * Main.h
 *
 *  Created on: 24 Nov 2024
 *      Author: EN . MAHMOUD TAMER
 */

#ifndef MAIN_H_
#define MAIN_H_

#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

// Pin definitions
#define TRIG1 PC6
#define ECHO1 PD4
#define TRIG2 PC7
#define ECHO2 PD3
#define TRIG3 PC3
#define ECHO3 PD2
#define TRIG4 PC2
#define ECHO4 PD5

// Function declarations
void ultrasonic_init(void);
uint16_t measure_distance(uint8_t trig_pin, uint8_t echo_pin);
uint16_t get_sensor1_distance(void);
uint16_t get_sensor2_distance(void);
uint16_t get_sensor3_distance(void);
uint16_t get_sensor4_distance(void);

#endif /* Main.H*/


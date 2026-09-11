#define LED_PIN 13

volatile bool trigger = false;
int led ;
String input = "";

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_PIN , OUTPUT);
  digitalWrite(LED_PIN, LOW);
  Serial.begin(9600);
    // Stop Timer1
  TCCR1A = 0;
  TCCR1B = 0;

  // Set compare match register for 0.5s at 16 MHz / 1024 prescaler
  // Formula: OCR1A = (16*10^6) / (1024*2) - 1 = 7812.5 -> use 7812
  OCR1A = 7812;

  // CTC mode
  TCCR1B |= (1 << WGM12);

  // Prescaler 1024
  TCCR1B |= (1 << CS12) | (1 << CS10);

  // Enable Timer1 compare interrupt
  TIMSK1 |= (1 << OCIE1A);

  // Enable global interrupts
  sei();

}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    char inChar = (char)Serial.read();  
    if (inChar == '\n' || inChar == '\r') {
        parseInput(input ); 
        input= "";        
    } 
    else {
      input += inChar;    
    }
    if (led == 0){
      digitalWrite(LED_PIN, LOW);
    }
    else{
      digitalWrite(LED_PIN, HIGH);
    }
  }
  if (trigger){
    Serial.println("Hi");
    trigger = false;
  }
}

ISR(TIMER1_COMPA_vect) {
  trigger = true;
}

void parseInput(String data) {

  float desired_angle;
  int speed;
  int horn_value;
  int aIndex = data.indexOf("A:");
  int bIndex = data.indexOf("B:");
  int cIndex = data.indexOf("C:");

  if (aIndex != -1 && bIndex != -1 && cIndex != -1) {
    desired_angle = data.substring(aIndex + 2, bIndex - 1).toFloat();
    speed = data.substring(bIndex + 2, cIndex - 1).toInt();
    led = data.substring(cIndex + 2).toInt();

    Serial.print("desired_angle: "); Serial.println(desired_angle);
    Serial.print("speed: "); Serial.println(speed);
    //Serial.print("HORN_S: "); Serial.println(HORN_S ? "true" : "false");
    
  } else {
    Serial.println("Invalid format! Expected A:val,B:val,C:val");
  }


}
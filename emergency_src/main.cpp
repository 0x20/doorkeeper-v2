
#include <SPI.h>
#define LOCKPIN         7          // Pin to door lock relais

void setup() {

  // Initialise Lock
  pinMode(LOCKPIN, OUTPUT);
  digitalWrite(LOCKPIN,LOW);
  delay(120000);
  digitalWrite(LOCKPIN,HIGH);
}


void loop() {

}

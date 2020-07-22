



boolean doorOpen = false;

/**
 * Send color to LEDs
 */
void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, c);
      strip.show();
      delay(wait);
  }
}

void setup() {

  // Initialize Serial comms
  Serial.begin(9600);
  while (!Serial);    // Do nothing if no serial port is opened
  String output = "{uid:'',access:0,doorstate:0}";
  Serial.println(output);

  // Initialize RFID reader
  SPI.begin();      // Init SPI bus
  mfrc522.PCD_Init();   // Init MFRC522
  //Serial.println(F("Init..."));
  //mfrc522.PCD_DumpVersionToSerial();  // Show details of PCD - MFRC522 Card Reader details

  // Initialise LEDs
  pinMode(LOCKPIN, OUTPUT);
  //delay(5000);
  digitalWrite(LOCKPIN,HIGH);
  pinMode(LEDGROUND, OUTPUT);
  digitalWrite(LEDGROUND,LOW);
  pinMode(LEDDATA, OUTPUT);
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  colorWipe(strip.Color(15, 0, 0), 10); // Red
}

/**
 * mfrc522.PICC_IsNewCardPresent() should be checked before 
 * @return the card UID
 */
String getID(){
  if ( ! mfrc522.PICC_ReadCardSerial()) { 
    return "0";
  }
  String userid;
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    // Get 2 character output for every hex value
    if(mfrc522.uid.uidByte[i] < 0x10)
    {
    userid += '0';
    }
    //Serial.print(mfrc522.uid.uidByte[i], HEX);
    userid += String(mfrc522.uid.uidByte[i], HEX);
  }
  // I want uid lengths to be defined as 14 characters, even if the card supports less.
  while(userid.length() < 14){
    userid += '0';
  }
  userid.toUpperCase();
  return userid;
}
/**
 * Check ID against known ID's
 */
boolean findID(String array[], String element) {
  #define ARRAYSIZE 100
  //Serial.println(readCard);
  for (int i = 0; i < (ARRAYSIZE); i++) {
    if (array[i].equalsIgnoreCase(element)) {
      return true;
    }
  }
  return false;
}

void doorUnlock(){
    digitalWrite(LOCKPIN, LOW);
    doorOpen = true;
    colorWipe(strip.Color(0, 0, 0), 10); colorWipe(strip.Color(0, 15, 0), 10); // LEDs Green
}

void doorLock(){
    digitalWrite(LOCKPIN, HIGH);
    doorOpen = false;
    colorWipe(strip.Color(0, 0, 0), 10); colorWipe(strip.Color(15, 0, 0), 10); // LEDs Red
}

void loop() {
  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
  if(mfrc522.PICC_IsNewCardPresent()) {
    String uid = getID();
    
    if(uid != "0"){
      //Serial.print("UID: "); Serial.println(uid);
      if(findID(goodKeys,uid)){
        //Serial.print("ACCESS: TRUE\n");
        if(doorOpen){
          doorLock();
          String output = "{uid:'" + uid + "',access:1,doorstate:0}";
          Serial.println(output);
    delay(2000);
        }else{
          doorUnlock();
          String output = "{uid:'" + uid + "',access:1,doorstate:1}";
          Serial.println(output);
    delay(2000);
        }
      }else{
        //Serial.print("ACCESS: FALSE\n");
        doorLock();
        String output = "{uid:'" + uid + "',access:0,doorstate:0}";
        Serial.println(output);
    delay(1000);
      }
    }
  }


}

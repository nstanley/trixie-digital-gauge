
#define clk_pin 4
#define data_pin 3
#define enable_pin 2

// Message format
const uint8_t MESSAGE_SIZE = 18; // 18 total bytes
const uint8_t header = 0xF0;     // Byte 0 = header
const uint8_t LABEL_START = 1;   // Byte 1 starts message, first line (label)
const uint8_t MAX_LABEL = 8;     // First line (label) is max 8 characters (last char at 8)
const uint8_t DATA_START = LABEL_START + MAX_LABEL; // Data starts after label on second line (9)
const uint8_t MAX_DATA = 7;      // Second line (data) is max 7 characters (last char at 16)
const uint8_t command = 0x1C;    // Byte 16 is the command byte
uint8_t checksum;                // Byte 17 is the checksum
uint8_t message[MESSAGE_SIZE];

// Demo messages
char lbl_fm[] = "   99.2";
char dta_fm[] = "FM1-1";
char lbl_wel[] = "WELCOME";
char dta_wel[] = "";
char lbl_speed[] = "SPEED";
char dta_speed[] = "30";
char lbl_maf[] = "MAF";
char dta_maf[] = "22.3";

bool sync = false;

void sendMessage() {
  // Send the data
  digitalWrite(enable_pin, HIGH);
  for (int i = 0; i < MESSAGE_SIZE; i++) {
    uint8_t data = message[i];

    for (int j = 0; j < 8; j++) {
      digitalWrite(clk_pin, HIGH);
      if (data & 0x80) {
        // Serial.print("1");
        digitalWrite(data_pin, LOW); // inverted logic
      }
      else {
        // Serial.print("0");
        digitalWrite(data_pin, HIGH); // inverted logic
      }
      data <<= 1;
      // if (j == 3) {
      //   Serial.print(" ");
      // }
      digitalWrite(clk_pin, LOW);
    }
    // Serial.print("  ");
    // Serial.print(message[i]);
    // Serial.print("\n");
  }
  digitalWrite(enable_pin, LOW);
  digitalWrite(clk_pin, HIGH);
  digitalWrite(data_pin, HIGH);
  // Serial.write("-------\n");
  delay(500);
}

void showData(char *label, char *data) {
  digitalWrite(enable_pin, HIGH);
  // Check lengths and truncate if necessary
  int lenLabel = strlen(label);
  if (lenLabel > MAX_LABEL) {
    lenLabel = MAX_LABEL;
  }
  int lenData = strlen(data);
  if (lenData > MAX_DATA) {
    lenData = MAX_DATA;
  }

  // message starts on second byte
  int j = 0;
  for (int i = LABEL_START; i < DATA_START; ++i) {
    if (i < LABEL_START+lenLabel) {
      message[i] = label[j];
    }
    else {
      message[i] = 0x20;
    }
    ++j;
  }
  j = 0;
  for (int i = DATA_START; i < (MAX_DATA + DATA_START); ++i) {
    if (i < DATA_START+lenData) {
      message[i] = data[j];
    }
    else {
      message[i] = 0x20;
    }
    ++j;
  }

  // calculate the checksum
  checksum = 0;
  for(int i = 0; i < MESSAGE_SIZE-1; i++){
    checksum += message[i];
  }
  checksum ^= 0xff;
  message[17] = checksum;

  digitalWrite(enable_pin, LOW);
  sendMessage();
}

void setup() {
  Serial.begin(9600);
  pinMode(clk_pin, OUTPUT);
  pinMode(data_pin, OUTPUT);
  pinMode(enable_pin, OUTPUT);
  message[0] = header;
  message[16] = command;
  digitalWrite(enable_pin, LOW);
  digitalWrite(clk_pin, HIGH);
  digitalWrite(data_pin, HIGH);
}

void loop() {
  // Demo messages
  showData(lbl_fm, dta_fm);
  delay(2000);
  showData(lbl_wel, dta_wel);
  delay(2000);
  showData(lbl_speed, dta_speed);
  delay(2000);
  showData(lbl_maf, dta_maf);
  delay(2000);
}

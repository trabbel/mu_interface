#define MAX_BUF 7

char buf[MAX_BUF];
int idx = 0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  bool command_valid = true;
  
  while (Serial.available() > 0) {  // While there is data in Serial buffer...
    command_valid = false;
    char in = Serial.read();        // Read a character.

    if (idx == MAX_BUF)
    {
      Serial.println("Buffer overrun!");
      idx = 0;
      buf[idx] = '\0';
    }

    if (in == ',')                   // If it is a ',' reset buf.
    {                 
      idx = 0;
      buf[idx] = '\0';
      command_valid = true;
    }
    else if (in == '*')                  // If it is a '*', print the current buffer.
    {                
      buf[idx] = '\0';
      Serial.println(buf);
      idx = 0;
      command_valid = true;
    } 
    else                            // Otherwise, add character to buf.
    {                        
      buf[idx] = in;
      idx++;
    }
  }

  if (!command_valid)
  {
    Serial.println("Command invalid");
  }

  delay(500);
}

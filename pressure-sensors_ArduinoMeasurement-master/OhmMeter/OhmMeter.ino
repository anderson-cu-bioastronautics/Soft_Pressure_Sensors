int analogPin= 0;
int raw= 0;
int Vin= 5;
float Vout= 0;
float R1= 10;
float R2= 0;
float buffer= 0;
float tm = 0;

void setup()
{
Serial.begin(9600);
pinMode(7,OUTPUT);
digitalWrite(7,HIGH);
analogReference(EXTERNAL);
}

void loop()
{
raw= analogRead(analogPin);
tm = millis();
if(raw) 
{
buffer= raw * Vin;
Vout= (buffer)/1024.0;
buffer= (Vin/Vout) -1;
R2= R1 * buffer;
//Serial.print("Vout: ");
//Serial.println(Vout);
//Serial.print("R2: ");
Serial.print(tm);
Serial.print("|");
Serial.print(R2);
Serial.print('\n');
delay(100);
}
}


#define A0 13
#define A1 12
int sensor1, sensor2, dato1, dato2;
void setup() {
  Serial.begin(9600,SERIAL_8N1, 3, 1);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
}

void loop() {
  sensor1 = analogRead(A0);
  sensor2 = analogRead(A1);

  dato1 = map(sensor1, 0, 4096, 0, 100);
  dato2 = map(sensor2, 0, 4096, 0, 100);

  Serial.print(dato1);
  Serial.print(',');
  Serial.println(dato2);

  delay(200);
}

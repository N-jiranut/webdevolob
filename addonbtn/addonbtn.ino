#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
const char* ssid     = "vivo_V25";
const char* password = "02_jiranut";
const char* svstart = "http://10.207.14.79:5000/start";
const char* svcancel = "http://10.207.14.79:5000/cancel";
const char* svsend = "http://10.207.14.79:5000/send";
unsigned long test;
const int startbtn = 15;
const int cancelbtn = 13;
const int sendbtn = 12;
int startc = HIGH;
int cancelc = HIGH;
int sendc = HIGH;

WiFiClient client;
HTTPClient http;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(startbtn, INPUT_PULLUP);
  pinMode(cancelbtn, INPUT_PULLUP);
  pinMode(sendbtn, INPUT_PULLUP);
  Serial.begin(9600);
  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi..");

  // Wait until connected
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("Connected to WiFi!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  int start = digitalRead(startbtn);
  int cancel = digitalRead(cancelbtn);
  int send = digitalRead(sendbtn);
  // Serial.println(send);
  // Serial.println(sendc);
  if (WiFi.status() == WL_CONNECTED) {
    if (start == HIGH && startc == LOW){
      http.begin(client, svstart);
      int httpResponseCode = http.POST("postData");
      Serial.println(httpResponseCode);
      http.end();
    }
    if (cancel == HIGH && cancelc == LOW){
      http.begin(client, svcancel);
      int httpResponseCode = http.POST("postData");
      Serial.println(httpResponseCode);
      http.end();
    }
    if (send == HIGH && sendc == LOW){
      http.begin(client, svsend);
      int httpResponseCode = http.POST("postData");
      Serial.println(httpResponseCode);
      http.end();
    }
  }
  Serial.println(send);
  startc = start;
  cancelc = cancel;
  sendc = send;
  delay(125); // ส่งทุก 100ms 
}

#include <Bridge.h>
#include <Process.h>

Process picture;
String filename;
int pir_pin = 8;
String path = "/mnt/sda1/";

void setup() {
  Bridge.begin();
  pinMode(pir_pin,INPUT);
}

void loop() {
  if (digitalRead(pir_pin) == true) {
    filename = "";
    picture.runShellCommand("date +%s");
    while(picture.running());
   
    while (picture.available()>0) {
      char c = picture.read();
      filename += c;
    } 
    filename.trim();
    filename += ".jpg";

    // Save the picture locally on a microSD located within the Arduino Yun
    picture.runShellCommand("fswebcam " + path + filename + " -r 1280x720");
    while(picture.running());
    Serial.println("File successfully saved locally!");

    // Upload to Amazon S3
    picture.runShellCommand("python " + path + "upload_picture.py " + path + filename);
    while(picture.running());
  }
}

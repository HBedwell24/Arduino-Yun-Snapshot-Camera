#include <Bridge.h>
#include <Process.h>

Process picture;
String filename;
int pir_pin = 8;
String path = "/mnt/sda1/";

Bridge.begin();

if (digitalRead(pir_pin) == true) {

	filename = "";
	picture.runShellCommand("date +%s");
	while(picture.running());
	 
	while (picture.available()>0) {
		char c = picture.read();
		filename += c;
	} 
	
	filename.trim();
	filename += ".png";
	
picture.runShellCommand("fswebcam " + path + filename + " -r 1280x720");
while(picture.running());
picture.runShellCommand("python " + path + "upload_picture.py " + path + filename);
while(picture.running());
	

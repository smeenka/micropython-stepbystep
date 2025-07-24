# Mechanotronica: Micropython cursus
***

## [Home](../micropython-cursus.md)

## Bluetooth

Voor deze test gaan we een HC05 bluetooth module gebruiken

![bluetooth module](../images/hc05_module.png)

De bluetooth module koppelen we aan poort 1 van de rp2040-rp-maker board.

Op de telefoon maken we gebruik van de app BT Car Controller
![Android app BT Car Controller ](../images/app_bt_car_controller.png)

Stappen:
* Installer de BT Car controller op je android telefoon
* Zet bluetooth aan en koppel de robot (in de lijst te vinden als DJO_ROBOT)
* Start de BT Car controller app
* In de app druk op de connect knop rechtsboven) en verbind met de DJO_ROBOT



### test 4.1 Eenvoudige bluetooth test

In de library vinden we het bluetooth object.

Eerst dienen we deze te importeren, en vervolgens te maken:

    from bluetooth import Bluetooth
    bt = Bluetooth()


Dan maken we de test

    def test_string():
      while True:
          time.sleep_ms(10)    
          line =  bt.readline()
          as_string = bt.line2string(line)
          if line:
              print("Regel:", as_string)

    print("Druk op toetsen in de bluetooth app op de telefoon")

    test_string()


### Zelf uitproberen:
  * druk op diverse knoppen in de BT Car controller en kijk of de ontvangen karakters overeenkomen met de verzonden karakters (te zien in de app!)
  * Zet de Advanced mode aan in de app (menu knop rechts boven) en kijk wat er nu verzonden wordt

### test 4.2 Bluetooth test met meerdere taken

  Een groot programma maken we door het programma in kleine taken te splitsen.

  Elke taak krijgt hierbij een enkele functie, die makkelijker te snappen en te testen is.

  We hebben in test_4_2_bluetooth_tasks de taken:

  | naam| functie| opmerking |
  | --- | --- | --- |
  |task_blink| hartbeat led| De hartbeat gebruiken om te zien of het programma nog aktief is|
  |task_bt_led| knipper als data ontvangen is via Bluetooth | De taak wordt aktief als de event_blink gezet is
  |task_bt_receive|Ontvangen en bekijken van Bluetooth data| Als data ontvangen is dat wordt task_bt_led aangezet door event_blink.set()
  
### taak voor het knipperen van de led als heartbeat van het programma

    async def task_blink():
      print("Start taak task_blink")  
      while True:
        led.on()
        await asyncio.sleep_ms(100)
        led.off()
        await asyncio.sleep_ms(900)

### taak voor knipperen van een led als een regel is ontvangen van bluetooth

    async def task_bt_blink():
      print("Start taak task_bt_blink")  
      while True:
        # wait until the bluetooth task does recieve a line
        await event_blink.wait()
        event_blink.clear()
        bt_led.value(0)
        await asyncio.sleep_ms(10)
        bt_led.value(1)

### taak voor het wachten op een BT regel en deze omzetting in een commando

De taak zal task_bt_blink wakker maken met de event_blink.set()

    async def task_bt_receive():
      print("Start taak task_bt_receive")
      while True:
        # zorg dat andere taken ook tijd krijgen
        await asyncio.sleep_ms(10)
        line =  bt.readline()
        if line:
          as_string = bt.line2string(line)
          if as_string:
            first_char = as_string[0]
            event_blink.set()
            
            if first_char == "U":
                print()"Licht Aan")
            ----    


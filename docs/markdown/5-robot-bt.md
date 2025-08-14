# Mechatronica: Micropython cursus
***

## [Home](../micropython-cursus.md)

## R2d2 besturen met de telefoon via de Dabble app

### Test test_5_1_robot_bt

Deze test bevat 2 taken
* task_blink
* task_command

De task_command wordt gestuurd door de dabble gamepad object.
In het eerste gedeelte worden de knoppen van de gamepad bekeken:

    async def task_command():
      print("Start taak task_command")
      rood = 0
      groen = 0
      blauw = 0
      global command # geef aan dat we de command op regel 20 willen gebruiken
      global neo
      while True:
        # zorg dat andere taken ook tijd krijgen
        await asyncio.sleep_ms(10)
        if gamepad.buttonPressed():
          if gamepad.isStart():
              print("Toeter")
              buzzer.setTone(400,100)
          if gamepad.isSelect():
              print("select")
              buzzer.mute()
          if gamepad.isSquare():
              print("Blauw aan")
              blauw = 100
          if gamepad.isTriangle():
              print("Rood Aan")
              rood = 100
          if gamepad.isCircle():
              print("Groen Aan")
              groen = 100
          if gamepad.isCross():
              print("kruisje")
              rood = 0
              groen = 0
              blauw = 0

In het 2e gedeelte wordt de richting en de snelheid van de robot uitgerekend. Hier is een beetje rekenkunde voor nodig. 

Het teken // dien je te lezen als: deel het gehele getal door een ander geheel getal, er zorg ervoor dat het resultaat ook een geheel getal (integer) is.

Voorbeeld: 
* p = 7 / 2 . Resultaat: p = 3.5 (p is een float)
* p = 7 // 2 . Resultaat: p = 3 (p is een integer)
 


        richting = gamepad.richting()
        snelheid = gamepad.snelheid()
        links = 0
        rechts = 0

        if richting >= 80 or richting <= -70:
            links = richting // 2
            rechts = richting // -2
        else:
            links = snelheid  + richting // 4 
            rechts= snelheid  - richting // 4
        robot.move(links, rechts)
        neo[0] = (rood, groen, blauw)
        neo[1] = (rood, groen, blauw)
        neo.write()



### Zelf uitproberen:
  * Zet de massa van de robot op 9 en kijk wat er gebeurt
  * Zet de massa van de robot op 0 en kijk wat er gebeurt
  * Verander zodanig dat telkens als je op een knop drukt de helderheid van de neopixel toe neemt.
  * Kies andere functies voor de knoppen, bijvoorbeeld verschillende geluiden of verschillende kleuren.
  * In de richting berekening zie je richting//4 Probeer andere getallen, en kijk wat het effect is.
  * Moeilijk: probeer de robot te besturen met de hoek en straal functies van de gamepad.

  


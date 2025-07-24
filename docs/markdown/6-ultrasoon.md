# Mechanotronica: Micropython cursus
***

## [Home](../micropython-cursus.md)

## Arduino

### Ultrasoon module

![Ultrasoon](../images/Ultrasoon%20sensor.png)

De ultrasoon sensor kan afstanden meten door het versturen van een ultrasone ping, en dan luisteren hoe lang het duurt voordat de ping weer ontvangen wordt.

Deze techniek is afgekeken van de vleermuizen.

### 6.1 Ultrasoon

Deze test laat een led knipperen afhankelijk van de gemeten afstand


De taak voor het meten van de afstand:

    async def task_distance():
      print("Start taak distance")
      sensor = HCSR04(trigger_pin=10, echo_pin=9)
      global distance
      while True:
        await asyncio.sleep_ms(200)
        distance = sensor.distance_mm()
        print('Distance:', distance, 'mm')  

In deze test wordt de sensor aangemaakt binnen de taak.

**global distance** betekent: we willen de waarde gebruiken die aan het begin van het programma staat op regel 13.
Deze waarde wordt door meerdere taken gedeeld.


### taak voor knipperen van een led die de afstand aangeeft

    async def task_distance_blink():
      print("Start taak distance_blink")
      distance_led = Pin(45, mode=Pin.OUT)
      global distance
      while True:
        await asyncio.sleep_ms(distance//2)
        distance_led.value(0)
        await asyncio.sleep_ms(10)
        distance_led.value(1)

Bij een afstand van 2 meter zal de led langzaam knipperen (1x per seconde). Bij een afstand van 1 meter (1000 mm) zal de led 2x per seconde knipperen.
Ook hier maken we gebruik van de gedeelde globale waarde **distance** 

### 6.2 Ultrasoon_r2d2

Deze test is gelijk aan 6.1 met een extra taak: het besturen van de r2d2 robot.

    async def task_robot():
        print("start taak task_robot")
        global r2d2
        global distance
        r2d2.move(50,50)
        
        achteruit = False
      
        while True:
            await asyncio.sleep_ms(10)
            if achteruit:
                if distance > 300:   # indien achteruit aan het rijden en de afstand is groter dan 30 cm ga weer voortuit rijden
                    achteruit = False
                    print("Vooruit")
                    r2d2.move(50,50)
            else:    
                if distance < 100:   # indien vooruit aan het rijden en de afstand is kleiner dan 10 cm, ga achteruit rijden
                    achteruit = True
                    print("Achteruit")
                    r2d2.move(0,-50) # motor langzaam achteruit met een draai




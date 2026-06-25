# HikerDeck

# My inspiration: 
My Instagram feed inspired me to make a cyberdeck, offline computers housed in cute compartments one could access offline. My sister had her birthday just a few weeks ago, so I wanted to gift her a cyberdeck she'd love. User needs: she is into hiking, reading, and learning new languages (currently Chinese). So I made a multilingual e-reading environment-sensing cyberdeck that would be useful on a hike. For example, it can load up a "hiking survival guide" on an offline e-reader and also tell you the altitude you are at in the hike in Chinese numerals. 

<img width="1776" height="1022" alt="image" src="https://github.com/user-attachments/assets/40ca1345-b739-4456-bed3-6bcaf5c753b0" />

# What does the project do?
The project is a dual-display cyberdeck optimized for hiking. It is an offline "mini computer" which can scroll through files such as a hiking survival guide. At the same time, on another display it can display the current pressure and altitude a hiker is at in Chinese lettering. The cyberdeck itself is controlled by 3 CherryMX switches and is housed inside a sunglass case! 
In summary, the main features include:
- Large screen displays hiking survival text uploaded by computer
- Small screen displays environmental data in Chinese lettering
- You can control back/forward pages and turning the small display on and off via 3 Cherry MX keys 

# Schematic:
Please note! The hikerdeck is currently perfboarded not PCBed! The entire wiring is contained inside the casing and once spread out it looks like this:
<img width="1235" height="784" alt="image" src="https://github.com/user-attachments/assets/a1266ec9-c9fb-4093-b475-64de4d5bee3d" />



# Firmware
The firmware adds on top of pre-existing sensor and display libraries (most notably gc and framebuffer) to display sensor values (like altitude) onto the small display. Using a custom-made Chinese bitmap font library, the firmware prints to the smaller display in Chinese lettering. At the same time, it also coordinates SPI activation between both the large and small displays which are wired onto the same SPI bus. The firware also takes the external buttons as inputs for when to switch display or when to switch pages on the larger display. The firware additionally calculates how many pages of hiking survival guide text there are on the large display and renders them onto the large display in an appropriate manner (without breaking up too much text or going off the page). 
Usage of each file is as following:
+ Pico_ePaper_2_7_V2.py --> library for the ePaper 2.7in V2 display (pre-existing) 
+ bmp280.py --> library for environment sensor (pre-existing) 
+ bmpWithSmallDisp.py --> module I made (which includes some pre-existing library code for 1.54'' display) which displays environmental stats in
+ Chinese lettering on the small display 
+ ChineseNum.py --> bitmap library I refer to in bmpWithSmallDisp.py helps me map characters onto small display 
+ main.py --> accepts button input, calculates and renders text info for the large display, controls SPI activation/switching, imports bmpWithSmallDisp to also switch to small display rendering 

# Layout:
I drew a small diagram to help you understand where everything fits inside the casing! 
<img width="2632" height="1374" alt="image" src="https://github.com/user-attachments/assets/7814a38a-f961-48ce-a666-6ec8edd1fc5b" />


# Casing:
Currently not 3D printed yet, but the CAD files are ready and I am using a cardboard case right now! 
<img width="600" height="500" alt="image" src="https://github.com/user-attachments/assets/67af89f6-8c0f-4604-bd48-797845a646aa" />

This is a cut open view of the whole case so you can see that there is a "top layer" where the displays are housed and a "bottom layer" with space for wiring and pico w. 


<img width="600" height="500" alt="image" src="https://github.com/user-attachments/assets/b8ba82ba-75e5-45cb-bcde-4d5465d836cb" />

^This is how the entire case would look assembled together, probably with screws to hold top and bottom layers in place. CAD folder has a 3D design version of the entire casing together and then parts of the casing which may be easier to CAD.


# How to build this?
1. Import firmware to VS code and connect pico w to VS code via pico extension on VS code 
3. Plug in the small display using the SPI1 pins on the pico w pinout (some specified in firmware) 
4. Plug in sensor via 12C pins on BMPE-280 sensor (refer to firmware for definitions!) 
5. Run the small display with sensor script and the firmware should both print environment data in terminal and show chinese version of that on small display (imports custom Chinese font library, framebuffer display etc etc) 
6. Plug in large display and wire up the 3 Cherry MX pins as well
7. Run the large display script (which imports the small display script and manages all SPI activation etc)
8. CAD casing from files and then screw the casing together
9. Fit all of the wiring inside the casing ! 

# How does it all fit together? 
The sunglass case has different "layers": 
The top layer is the two displays which live on the lid 
Below that, there are 3 mounted CherryMX switches and a port to connect to the pico underneath. 
And on the very bottom under the switches there's the perfboard where the raspberry pico w, battery, and environment sensor live. 

<img width="678" height="972" alt="image" src="https://github.com/user-attachments/assets/e5e1e2ea-ae3e-4d67-8cb4-797d9b7f6b5b" />


# BOM 
SR. No	Items	Quantity	Unit Price	Total Price	URL
1	Raspberry Pico W	1	$6.00	$6.00	https://www.digikey.com/en/products/detail/raspberry-pi/SC0918/16608263
2	E-paper Display Waveshare 2.7in Version 2.2 + 8 Pin Header	1	$18.95	$18.95	https://www.amazon.com/Display-Raspberry-Arduino-200x200-Interface/dp/B0DCYZS5BC/ref=sr_1_2?crid=226FPRV9VCF06&dib=eyJ2IjoiMSJ9.98kAT0g67KxKBucByNFecZB1nF47u8bZJCAO4ysvo9RrHcnjZFJLQE3xDZMs3EE132TUiFJJjdxqDkLtLrn14a2y4qKYXGnheVdWL_Iirih1Wufw-bHQgzVBC3iwb6sXMuYsiW7CCzP9o4N8OEbltC3cdX0t4t6MM8yMP7vnn4vJDzEJiFX5ZllrAXJ-U8ZQ0K3rkIVB6x686RY0VUpy9nIJVFl5WCiPs4hva2aTfho.TaOn-1ulH-Ulg-UsMeqbGm0eDYkfaPdBGgYeEkRNmIM&dib_tag=se&keywords=e-paper+mini+screen&qid=1779568258&sprefix=e-paper+mini+screen+%2Caps%2C123&sr=8-2
3	E-paper Display Waveshare 1.54in Version 1.2 + 8 Pin Header	1	$27.99	$27.99	https://www.amazon.com/2-7inch-HAT-Resolution-Electronic-Communicating/dp/B075FQKSZ9/ref=sr_1_4?crid=1YEDTIZCGIHC5&dib=eyJ2IjoiMSJ9.MkWONqJEJMXL7EeR_VqIMI0mskpZAIRGp-sOJKn15f3ha55h1-D_fB6ar5EhX6yM0fXr1RzKdYtbYLuQbARliqQzYzsqwNc2FlaUoW36qx-te8946rYBDoRsMVcfqcel4fdEfFjjM9CW37EfUj0apTxiPLjqY-c0i6mha94uZ3d4cKAVLZsRg9n_FctjgvRSClhwjxikwAAq8SME739xo9wA2JDA-SIgOOpkuWf8rcQ.qEbtBHSm-gqOTC4SNgwUyNB_hhtczFgw8zPAuQd29Ac&dib_tag=se&keywords=Waveshare+2.7inch+E-Ink+Display+Module&qid=1779569280&sprefix=waveshare+2.7inch+e-ink+display+module%2Caps%2C163&sr=8-4
4	Sunglass case	1	$7.99	$7.99	self sourced
5	Perfboard 2.36inx1.57in	1	$1.89	#1.89	https://www.amazon.com/QSYZAIL-Perfboard-Compatible-Soldering-Protoboard/dp/B0G4QTPVZ8/ref=sr_1_2_sspa?crid=2P8ZRO2I1NXGB&dib=eyJ2IjoiMSJ9.M8d2MJLl8AKNjMwCTp0yFC0ME6G8zfO4gvUo6L0jIGGx_wnCGgM8lQp7hlAXMXPnMXKau2CMub9if_eqzj1cSMVj4EyKvyP8evmZoOnde9HTvQcrYAM7IKdfKK3DFIiwvoalyWazEzmIPnnKmfwvt-dr0D_M4q8okxlPfiDC8d93XiDwaUwZY-IMiUC2O6GofukJ47_V-0WYtSF08Dn8xJEjAON2fU_wiiG7csqa_N4.kCoNEuowSr_RrcXdWONYP5epzTGgEgUyBwwbLB-B7Yc&dib_tag=se&keywords=perfboard&qid=1782333543&sprefix=perfb%2Caps%2C463&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1
7	GY-BMPE280 Sensor	1	$6.99	$6.99	https://www.amazon.com/Atmospheric-Pressure-Temperature-Humidity-GY-BME280/dp/B0DHPCFJD6/ref=sr_1_10?dib=eyJ2IjoiMSJ9.e_GjIvhBjSbWD8WF9xrJUMNWPPxWbG0MXjbnFQmEe8HRNLzufZ_m0UWhpkfiR7dfR9jlF3FNKRCkyh-dC5t5QP5tBRwrNmEamCs9IF8KOX5OnvtaaQpta1t4JYtR9AvntXXrMlcDBN5HTEAuKV59jT5MYSLVlSOfqznUNa8ahZATV5vXsYJPGZ8HqaYi3EwzRYo1uuHYJo9nfroMo49HwOkA7GfNfV5FAm-I5cmxv50.w_6bA4F7KdXcDlMuKgrQSGmmIarEpHfajHYqlgIJmNg&dib_tag=se&keywords=i2c%2Btemperature%2Bsensor&qid=1779573060&sr=8-10&th=1
8	CherryMX switches	3	$0.44	$1.33	https://www.amazon.com/Cherry-Mechanical-Keyboard-Switches-Noticeable/dp/B0FYR9Z777/ref=sr_1_1_sspa?crid=258S0CKHWJ7KO&dib=eyJ2IjoiMSJ9.BJOR7UjzVwAi9dwLvX0xg2kxr_0v6ka9V8xO_J8Pnk3HVHHewCzfBSIg3gcA0iZaNKvwB_rOU6iVkaR8KeRPE921DkPDIlnl9nUS5567vIf34oV3kAybrfE7W137iuuUSauMjqtigMWQHgBpiS-CZRolO6jOWXlI1drjax9ssP398osQkLtJzyYteKJl0nb0Okwh-XQR8-_skLy9sBHKgzEBtU1YRF5KsbXQMDtBioo.8a8IhgzvNoBK9NwUgTGo7SFJVD3p84jZvQz1e8Z4v7I&dib_tag=se&keywords=cherry+mx+switches&qid=1782333643&sprefix=cherry+mx+swithes%2Caps%2C287&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1
Total	8	9		$82.25?	

**here is the link to my demo video!:** https://youtu.be/0BxvbPZM9zg

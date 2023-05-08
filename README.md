# Talking multimeter project 
This tool allows a visually impaired or blind user to access the measurements provided by an OWon 16 multimeter.

## Functionalities 
This application allows to :
* display the measured values on the screen in large characters
* verbally announce the measured values and units
* the keyboard shortcut "F4" indicates the status of the BLE link
* the keyboard shortcut "F5" announces the value of the measurement

two json configuration files are used :
* for protocol data exchange (measurements, data type and units, and gain)
* tool configuration (background and dont colors, font size, etc) 

## Accessibility 
this tool is fully accessible with the NVDA screen reader.

## Source code 
this application has been developed in python 3. the GUI is based on the WX python library to ensure its accessibility.

folowing modules are used :
* pyttsx3 : voice générator
* WXpython : graphical interface
* wxasync: thread managment 
* asyncio : async managment 

## License 
this tool is developed under CECIL license. 
it is free and open source.
any modification of the code have to be published in the same terms.
 
## Developers
This tool has been developped by 2 members of "l'atelier partagé" FABLAB located in Betton (Bretagne France), with the support of "My Human Kit" (MHK), FABLAB located in Rennes (Bretagne France).
* Developper : Sebastien B.
* user : François LB


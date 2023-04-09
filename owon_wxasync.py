import wx
import asyncio
import wxasync
from bleak import BleakClient,  BleakGATTCharacteristic, BleakScanner, BleakError
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
import time
import pyttsx3

#OWON 16
MODEL_NAME="BDM"
MODEL_ADDR="A6:C0:80:90:2D:DB"
CHAR_NBR_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"

def parle (chaine):
    engine.say(chaine)
    engine.runAndWait()

dict = {"25": ("milli Volts",10),
        "35": ("Volts",1000),
        "33": ("Ohm",10),
        "41": ("Kilo Ohm",10),
        "51": ("Mega Ohm",1000),
        "74": ("nanoFarad",10),
        "163": ("Hertz",10),
        "32": ("°C",1),
        "96": ("NCV",10),
        "145": ("micro Ampere",10),
        "154": ("milli Ampere",100),
        "162": ("Hertz",100)}



 #Windows closing handler
def on_close(event):
    #asyncio.create_task(self.ble.disconnect_async())
    #event.Skip()
    # cancelling all tasks effectively ends the program
    print("on close event called")
    for task in asyncio.all_tasks():
        task.cancel()

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='OWON Bluetooth connexion', size=(800, 600))
        
        #cree la fenetre au centre de l'ecran
        self.Centre()
        self.panel = wx.Panel(self)
        
        #couleur et taille
        self.font = wx.Font(90, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.panel.SetForegroundColour((255,255,0))
        self.panel.SetBackgroundColour((0,0,0))
        self.panel.SetFont(self.font)
        
        self.mesure_label = wx.StaticText(self.panel,label="")        
        self.mesure_valeur = wx.StaticText(self.panel, style=wx.ALIGN_CENTRE_HORIZONTAL|wx.ST_NO_AUTORESIZE,label="")
        
        #self.text_ctrl = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.mesure_label, 0, wx.EXPAND, 5)
        self.sizer.Add(self.mesure_valeur, 1, wx.EXPAND, 5)
        
        #self.sizer.Add(self.text_ctrl, 1, wx.EXPAND)
        self.panel.SetSizer(self.sizer)
        
        self.selecteur = "none"
        
        self.connected=False
        

    async def main_loop(self):
       
        #Disconnect Handler
        async def handle_disconnect(_: BleakClient):
            print("Device was disconnected, goodbye.")
            """
            self.mesure_valeur.SetLabel("Connecting")
            parle ("En attente de connexion")
            while self.device is None:
                #self.mesure_valeur.AppendText(".")
                #self.device = await BleakScanner.find_device_by_filter(filter_bluetooth_device)
                self.device = await BleakScanner.find_device_by_name(MODEL_NAME)
            # cancelling all tasks effectively ends the program
            #for task in asyncio.all_tasks():
                #task.cancel()
            """
            
        def decode_value (data: bytearray):
            print(f"{data[0]}",f"{data[1]}",f"{data[2]}",f"{data[3]}",f"{data[4]}",f"{data[5]}")
            
            selecteur,facteur=dict[str(data[0])]
            
            if data[5] < 128:
                value = str(((data[5]*256 + data[4])/facteur) )
            else:
                value = "-"+str(((((data[5]-128)*256 + data[4])/facteur)))
                
            return (f"{selecteur}", f"{value} {selecteur}")
          
    
        #Receiving data from Bluetooth Handler
        def handle_rx(_: BleakGATTCharacteristic, data: bytearray):
            #print("received:", data.decode())
            #self.mesure_label.SetLabel("Selecteur: Volts")
            #self.mesure_valeur.SetLabel(data.decode())
            if data is not None:
                print("received:", decode_value(data))
                selecteur,value=decode_value(data)
                self.mesure_label.SetLabel("Selecteur: "+selecteur)
                if selecteur != self.selecteur:
                    self.selecteur = selecteur
                    parle (selecteur)
                self.mesure_valeur.SetLabel(value)
             
              
        #wait for connexion
        while True:
            self.device = None
            self.mesure_valeur.SetLabel("Connecting")
            parle ("En attente de connexion")
            while self.device is None:
                #self.mesure_valeur.AppendText(".")
                #self.device = await BleakScanner.find_device_by_filter(filter_bluetooth_device)
                self.device = await BleakScanner.find_device_by_name(MODEL_NAME)

            #Device connected
            self.mesure_valeur.SetLabel("Connected")
            parle ("Connecté")
            print ('device found')
            time.sleep(2)
            
            # Waiting for data loop
            async with BleakClient(self.device, disconnected_callback=handle_disconnect) as client:
                self.mesure_valeur.SetLabel("En attente de données")
                parle("En attente de données")
                #print ('start notify')
                #wxasync.AsyncBind(wx.EVT_CLOSE, on_close)
                await client.start_notify(CHAR_NBR_UUID, handle_rx)
                self.connected = await client.is_connected()
                while self.connected:
                    await asyncio.sleep(5.0)
                    self.connected = await client.is_connected()
                    #await client.stop_notify(CHAR_NBR_UUID)
                    #print ('end notify')
                    
            parle("Multimètre déconnecté   ")                    
            print ('sortie de boucle')
            
        """
        await asyncio.gather(
            self.read_from_ble(),
            wxasync.AsyncBind(wx.EVT_CLOSE, self.on_close),
        )
        """


if __name__ == '__main__':
    engine = pyttsx3.init()
    engine.setProperty("rate", 178)
    app = wxasync.WxAsyncApp()
    frame = MyFrame()
    frame.Show()
    loop = asyncio.get_event_loop()
    loop.create_task(frame.main_loop())
    loop.run_until_complete(app.MainLoop())
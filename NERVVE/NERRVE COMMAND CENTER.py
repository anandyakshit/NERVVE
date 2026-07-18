import customtkinter as ctk
import serial
import threading
from datetime import datetime

#variables(probably_global)
packet_count = 0
cntn = ""
#serial_data_reader
ser = serial.Serial("COM3",9600)
def serial_listener():
    
    while True:
        
        try:
            packet = ser.readline().decode("utf-8", errors="ignore").strip()
            
            if packet:
                print(packet)
                result = parse_packet(packet)
                global cntn
                cntn = "Connected"
                
                if result:
                    msg, lat, lon = result
                    app.after(0,lambda:update_dashboard(msg,lat,lon))
            else:
                cntn = "Disconnected"
        except Exception as e:
            print(e)
            
#serial_data_parser
def parse_packet(packet):
    try:
         parts = packet.split("|")
         msg = parts[0].replace("SOS:","").strip()
         lat = parts[1].replace("LAT:","").strip()
         lon = parts[2].replace("LONG:","").strip()
         return msg, lat, lon
        
    except Exception as e:
        print("Parse Error:",e)
        return None

#dashboard_updater
def update_dashboard(msg, lat, lon):

    #alert_history_updater
    timestamp= datetime.now().strftime("%H:%M:%S")
    history_entry = (f"[{timestamp}]" ,f"[{msg}]\n")
    history_box.insert("end", history_entry)
    history_box.see("end")

    #packet_counter
    global packet_count
    packet_count += 1
    
    
    #main_update
    priority_label.configure(text="Priority: High")
    message_box.delete('1.0','end')
    message_box.insert('1.0', msg)
    location_label.configure(text=f"Latitude: {lat}\nLongitude: {lon}")

            
#appearence
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("NERVVE Command Centre")
app.geometry("1200x700")

#header

header = ctk.CTkFrame(app, height=80)
header.pack(fill="x", padx=10, pady=10)

title = ctk.CTkLabel(header, text="NERVVE COMMAND CENTRE", font=("Arial", 28, "bold"))
title.pack(side="left", padx=20, pady=20)

status = ctk.CTkLabel(header, text="🟢 ONLINE", font=("Arial", 18, "bold"))
status.pack(side="right", padx=20)

#Maine_Area

main = ctk.CTkFrame(app)
main.pack(fill="both", expand=True, padx=10, pady=10)

#left_panel

left_panel = ctk.CTkFrame(main, width=250)
left_panel.pack(side="left",fill="y", padx=10, pady=10)

ctk.CTkLabel(left_panel,text="SYSTEM STATUS",font=("Arial", 20, "bold")).pack(padx=20,pady=20)

ctk.CTkLabel(left_panel,text="Receiver Status:").pack(pady=10)
ctk.CTkLabel(left_panel,text=cntn).pack(pady=5)


ctk.CTkLabel(left_panel,text="Packets Recieved:").pack(pady=10)
ctk.CTkLabel(left_panel,text="0").pack(pady=5)


#center_panel

center_panel = ctk.CTkFrame(main)
center_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

ctk.CTkLabel(center_panel,text="ACTIVE ALERT",font=("Arial", 24, "bold")).pack(pady=20)

priority_label = ctk.CTkLabel(center_panel,text="Priority: NONE",font=("Arial", 22, "bold"))
priority_label.pack(pady=10)

message_box = ctk.CTkTextbox(center_panel,height=200)
message_box.pack(fill="x", padx=20, pady=20)
message_box.insert("1.0","Waiting for incoming packets...")

location_label = ctk.CTkLabel(center_panel,text="Latitude: --\nLongitude: --",font=("Arial", 18))
location_label.pack(pady=20)

open_map = ctk.CTkButton(center_panel,text="Open Location")
open_map.pack(pady=20)

# RIGHT PANEL

right_panel = ctk.CTkFrame(main, width=300)
right_panel.pack(side="right", fill="y", padx=10, pady=10)

ctk.CTkLabel(right_panel,text="ALERT HISTORY",font=("Arial", 20, "bold")).pack(pady=20)

history_box = ctk.CTkTextbox(right_panel)
history_box.pack(fill="both",expand=True,padx=10,pady=10)

history_box.insert("1.0","No alerts received.")
threading.Thread(target=serial_listener, daemon=True).start()
app.mainloop()

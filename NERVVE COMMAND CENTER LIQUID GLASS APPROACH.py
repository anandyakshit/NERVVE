import customtkinter as ctk
import serial
import time
from serial.tools import list_ports
import threading
from datetime import datetime
import webbrowser
import pywinstyles

#variables(probably_global)
packet_count = 0
cntn = ""
ser = None
alerts = []
current_lat = ""
current_lon = ""
running = True

#appearence
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
app = ctk.CTk()
app.title("NERVVE Command Centre")
app.geometry("1200x700")

#acrylic Background (BETA)
pywinstyles.apply_style(app, "aero")
pywinstyles.change_header_color(app, "#0B0F14")
pywinstyles.change_title_color(app, "white")
pywinstyles.change_border_color(app, "#00AEEF")
#Main_Area
main = ctk.CTkFrame(app, fg_color="transparent")
main.pack(fill="both", expand=True)
main.grid_columnconfigure(0,weight=1)
main.grid_columnconfigure(1,weight=3)
main.grid_columnconfigure(2,weight=2)
main.grid_rowconfigure(0,weight=1)


test = ctk.CTkFrame(
    main,
    width=500,
    height=300,
    fg_color="transparent",
    corner_radius=30
)

test.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)

#location_opener
def open_location(lat, lon):
    url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=16/{lat}/{lon}"
    webbrowser.open(url)

#destry_threads
def on_closing():
    global running
    global ser
    print("shutting down...")
    running = False
    try:
        if ser is not None:
            ser.close()
    except:
            pass
    app.destroy()    

#connection_manager
def find_arduino():

    ports = list_ports.comports()

    print("\n Available ports:")

    for port in ports:

        print(
            port.device,"|",
            port.description
        )

        try:

            s = serial.Serial(
                port.device,
                9600,
                timeout=1
            )

            print("Connected to", port.device)

            return s

        except Exception as e:

            print(
                "Failed:",
                port.device,
                e
            )

    return None

def connection_manager():
    global ser
    while running:
        print("Connection Manager running...")
        if ser is None:
            print("Searching for Arduino...")
            try:
                ser = find_arduino()
                if ser:
                    print("Arduino Connected")
                    app.after(0,lambda: connection_status.configure(text="Connected"))
                    app.after(0,lambda: status_box.configure(fg_color="green"))
            except:
                pass
        time.sleep(2)
                
                                             
#serial_data_reader
def serial_listener():
    global ser
    while running:
        if ser is None:
            time.sleep(1)
            continue
        
        try:
            packet = ser.readline().decode("utf-8",errors="ignore").strip()
            if packet:
                result = parse_packet(packet)
                if result:
                    msg, lat, lon = result
                    app.after(0,lambda:update_dashboard(msg, lat, lon))
        except Exception as e:
            print("Arduino Disconnected")
            try:
                ser.close()
            except:
                pass
            ser = None
            app.after(0,lambda:connection_status.configure(text="Disconnected"))
            app.after(0,lambda:status_box.configure(fg_color="red"))
            
            
#serial_data_parser
def parse_packet(packet):
    try:
         parts = packet.split("|")
         msg = parts[0].replace("DATA: SOS:","").strip()
         lat = parts[1].replace("LAT:","").strip()
         lon = parts[2].replace("LONG:","").strip()
         if not msg:
             msg = "No message provided"
         return msg, lat, lon
        
    except Exception as e:
        print("Parse Error:",e)
        return None

#dashboard_updater
def update_dashboard(msg, lat, lon):
    
    #packet_counter
    global packet_count
    packet_count += 1
    print(packet_count)
    pkt_count_label.configure(text=str(packet_count))   
    
    #alert_history_updater
    global current_lat
    global current_lon
    current_lat = lat
    current_lon = lon
    timestamp= datetime.now().strftime("%H:%M:%S")
    alerts.append({
    "timestamp": timestamp,
    "message": msg,
    "lat": lat,
    "lon": lon
    })

    add_alert_card(
    timestamp,
    msg,
    lat,
    lon
    )

    
    #main_update
    priority_label.configure(text="Priority: High")
    message_box.delete('1.0','end')
    message_box.insert('1.0', msg)
    location_label.configure(text=f"Latitude: {lat}\nLongitude: {lon}")

#footer
footer = ctk.CTkFrame(app, height=80,fg_color="#080C12", corner_radius=15, border_width=1, border_color="#00FFAA")
footer.pack(fill="x", padx=10, pady=10)
title = ctk.CTkLabel(footer, text="NERVVE COMMAND CENTRE", font=("Arial", 28, "bold"))
title.pack(side="left", padx=20, pady=20)
online = ctk.CTkLabel(footer, text="Beacon Online",font=("Comic Sans",18,"bold"))
online.pack(side="right",padx=20,pady=20)


#left_panel

#left_panel

left_panel = ctk.CTkFrame(
    main,
    width=220,
    fg_color="#10141C",
    corner_radius=15,
    border_width=1,
    border_color="#30363D"
)

left_panel.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=20,
    pady=20
)


ctk.CTkLabel(
    left_panel,
    text="SYSTEM STATUS",
    font=("",20,"bold")
).pack(
    padx=20,
    pady=20
)


ctk.CTkLabel(
    left_panel,
    text="Receiver Status:"
).pack(
    pady=10
)


status_box = ctk.CTkFrame(
    left_panel,
    fg_color="red",
    corner_radius=10
)

status_box.pack(
    pady=5
)


connection_status = ctk.CTkLabel(
    status_box,
    text="Disconnected",
    font=("Arial",16,"bold"),
    text_color="white"
)

connection_status.pack(
    padx=20,
    pady=8
)


ctk.CTkLabel(
    left_panel,
    text="Total Alerts Received:",
    font=("Arial",15,"bold")
).pack(
    pady=100
)


pkt_count_label = ctk.CTkLabel(
    left_panel,
    text="0",
    font=("Arial",26,"bold")
)

pkt_count_label.pack()

left_panel.pack_propagate(False)


#center_panel

center_panel = ctk.CTkFrame(
    main,
    fg_color="#10141C",
    corner_radius=15,
    border_width=1,
    border_color="#00FFAA"
)

center_panel.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=20,
    pady=20
)

ctk.CTkLabel(center_panel,text="ACTIVE ALERT",font=("Arial", 24, "bold")).pack(pady=20)

priority_label = ctk.CTkLabel(center_panel,text="Priority: NONE",font=("Arial", 22, "bold"))
priority_label.pack(pady=10)

message_box = ctk.CTkTextbox(center_panel,height=200,fg_color="#05070A",border_width=1,border_color="#30363D")
message_box.pack(fill="x", padx=20, pady=20)
message_box.insert("1.0","Waiting for incoming packets...")

location_label = ctk.CTkLabel(center_panel,text="Latitude: --\nLongitude: --",font=("Arial", 18))
location_label.pack(pady=20)


#location_opener
def open_current_location():

    if current_lat and current_lon:

        open_location(
            current_lat,
            current_lon
        )

open_map = ctk.CTkButton(
    center_panel,
    text="📍 Open Current Location",
    command=open_current_location,
    fg_color="dark green"
)

open_map.pack(pady=20)
center_panel.pack_propagate(False)

#right_panel

right_panel = ctk.CTkFrame(
    main,
    fg_color="#10141C",
    corner_radius=15,
    border_width=1,
    border_color="#30363D"
)

right_panel.grid(
    row=0,
    column=2,
    sticky="nsew",
    padx=20,
    pady=20
)


ctk.CTkLabel(right_panel,text="ALERT HISTORY",font=("Arial", 20, "bold")).pack(pady=20)

history_box = ctk.CTkScrollableFrame(right_panel)
history_box.pack(fill="both",expand=True,padx=10,pady=10)


right_panel.pack_propagate(False)

#history_alert_card
def add_alert_card(timestamp, msg, lat, lon):

    card = ctk.CTkFrame(history_box)

    card.pack(
        fill="x",
        padx=5,
        pady=5
    )

    ctk.CTkLabel(
        card,
        text=f"🚨 {timestamp}",
        font=("Arial", 14, "bold")
    ).pack(anchor="w", padx=10, pady=(10, 0))

    ctk.CTkLabel(
        card,
        text=f"💬 {msg}",
        wraplength=300,
        justify="left"
    ).pack(anchor="w", padx=10)

    ctk.CTkLabel(
        card,
        text=f"📍 {lat}, {lon}"
    ).pack(anchor="w", padx=10)

    ctk.CTkButton(
        card,
        text="Open Location",
        command=lambda: open_location(lat, lon)
    ).pack(
        anchor="e",
        padx=10,
        pady=10
    )


#main_processes
threading.Thread(target=connection_manager,daemon=True).start()
threading.Thread(target=serial_listener, daemon=True).start()
app.protocol("WM_DELETE_WINDOW",on_closing)
app.mainloop()

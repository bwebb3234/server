import tkinter as tk
from scapy.all import sniff, wrpcap

class PacketSnifferApp:
    def __init__(self, master):
        self.master = master
        master.title("Packet Sniffer")

        self.packets = []
        self.sniffer = None
        self.is_sniffing = False

        self.interface_label = tk.Label(master, text="Interface:")
        self.interface_label.pack()
        self.interface_entry = tk.Entry(master)
        self.interface_entry.insert(0, "eth0")  # change as needed
        self.interface_entry.pack()

        self.promisc_var = tk.IntVar()
        self.promisc_check = tk.Checkbutton(master, text="Promiscuous Mode", variable=self.promisc_var)
        self.promisc_check.pack()

        self.start_button = tk.Button(master, text="Start Sniffing", command=self.start_sniffing)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop Sniffing", state=tk.DISABLED, command=self.stop_sniffing)
        self.stop_button.pack()

        self.status_label = tk.Label(master, text="Status: Idle")
        self.status_label.pack()

    def packet_handler(self, packet):
        self.packets.append(packet)
        print(packet.summary())

    def start_sniffing(self):
        if self.is_sniffing:
            return
        iface = self.interface_entry.get()
        promisc = bool(self.promisc_var.get())
        self.packets = []
        self.is_sniffing = True
        self.status_label.config(text="Status: Sniffing...")

        # Set promiscuous mode using system call
        if promisc:
            import os
            os.system(f"ip link set {iface} promisc on")

        # Start sniffing asynchronously to not block the GUI
        from threading import Thread
        def sniff_thread():
            sniff(iface=iface, prn=self.packet_handler, store=False, stop_filter=lambda x: not self.is_sniffing)
        self.sniffer = Thread(target=sniff_thread)
        self.sniffer.start()

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_sniffing(self):
        if not self.is_sniffing:
            return
        self.is_sniffing = False
        iface = self.interface_entry.get()

        # Disable promiscuous mode when stopping
        import os
        os.system(f"ip link set {iface} promisc off")

        self.status_label.config(text=f"Status: Stopped. Captured {len(self.packets)} packets.")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        # Save packets to pcap
        if self.packets:
            wrpcap("capture.pcap", self.packets)
            print(f"Saved {len(self.packets)} packets to capture.pcap")

if __name__ == "__main__":
    root = tk.Tk()
    app = PacketSnifferApp(root)
    root.mainloop()
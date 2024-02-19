# adapted from StackOverflow: https://stackoverflow.com/questions/55929578/python-using-pyshark-to-parse-pcap-file

import pyshark
import os
import pandas as pd
import sys

# fname = 'los_1_iphone_tethering_in_lab'
# fname = 'los_3_ap_in_lab'
fname = sys.argv[1]
capture = pyshark.FileCapture(fname)

phy_col, data_rate_col, channel_col, freq_col, signal_col, noise_col, snr_col, tx_addr, timestamp_col, duration_col, ifs_col, start_tsf_col, end_tsf_col = \
	[], [], [], [], [], [], [], [], [], [], [], [], []
# print(pkt.layers)
# print(pkt.wlan_radio.field_names)

for pkt in capture:
	phy_col.append(pkt.wlan_radio.phy)
	# print(pkt.wlan_radio.11g_mode)
	data_rate_col.append(pkt.wlan_radio.data_rate)
	channel_col.append(pkt.wlan_radio.channel)
	freq_col.append(pkt.wlan_radio.frequency)
	signal_col.append(pkt.wlan_radio.signal_dbm)
	noise_col.append(pkt.wlan_radio.noise_dbm)
	snr_col.append(pkt.wlan_radio.snr)
	try: # wlan.fixed.src_mac_addr, wlan.sa, wlan.fixed.sa
		tx_addr.append(pkt.wlan.ta)
	except AttributeError:
		tx_addr.append(None)
	timestamp_col.append(pkt.wlan_radio.timestamp)
	duration_col.append(pkt.wlan_radio.duration)
	try:
		ifs_col.append(pkt.wlan_radio.ifs)
	except AttributeError:
		ifs_col.append(None)
	start_tsf_col.append(pkt.wlan_radio.start_tsf)
	end_tsf_col.append(pkt.wlan_radio.end_tsf)

data = {'phy': phy_col, 'data_rate': data_rate_col, 'channel': channel_col, 'frequency': freq_col, \
	'signal_dbm': signal_col, 'noise_dbm': noise_col, 'snr': snr_col, "tx_addr": tx_addr, 'timestamp': timestamp_col, 'duration': duration_col,\
		 'ifs': ifs_col, 'start_tsf': start_tsf_col, 'end_tsf': end_tsf_col}

df = pd.DataFrame(data)
print(df.shape)
df.to_csv(fname[:-5] + '.csv')

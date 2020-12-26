import obspy
from obspy.signal.trigger import classic_sta_lta, plot_trigger, trigger_onset
import numpy as np



st = obspy.read("200428000000-CH0.mseed")[0]

t = st.stats.starttime
t1 = t + 3600 * 13
#t1 = t
#t2 = t + 3600 * 13
t2 = st.stats.endtime
trace = st.trim(t1,t2)
#trace = st
#print(trace.data)
trace.data = trace.data/6553.6
#print(trace.data)
trace.filter('bandpass', freqmin = 5, freqmax = 20)
df = trace.stats.sampling_rate

cft = classic_sta_lta(trace.data, int(10 * df), int(70 * df))
on_of = trigger_onset(cft, 1.15, 0.5)
#print(trace.stats)
#print(trace.data)
print(on_of)
np.savetxt("eventosp10.txt", on_of)
plot_trigger(trace, cft, 1.15, 0.5)
from obspy import read
DATA = 'waveforms/{}_{}_{}.mseed'

def get_waveforms(network=None, station=None, location=None, channel=None, starttime=None, endtime=None, event=None):
    id_ = event.resource_id.id.split('/')[-1]
    channel = 'H' + channel[1:]  # file names do not fit the channel code
    fname = DATA.format(id_, station, channel)
    stream = read(fname, 'MSEED')
    stream.trim(starttime, endtime)
    return stream
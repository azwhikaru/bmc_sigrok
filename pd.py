import sigrokdecode as srd

class SamplerateError(Exception):
    pass

class Decoder(srd.Decoder):
    api_version = 3
    id = 'bmc'
    name = 'Biphase Mark Code'
    longname = 'Biphase Mark Code'
    desc = 'Biphase Mark Code decoder.'
    license = ''
    inputs = ['logic']
    outputs = ['bmc']
    tags = ['Encoding']

    channels = (
        {'id': 'data', 'name': 'Data', 'desc': 'BMC Data Input'},
    )
    annotations = (
        ('bit-0', 'Bit 0'),
        ('bit-1', 'Bit 1'),
    )
    annotation_rows = (
        ('bits', 'Bits', (0, 1)),
    )

    def __init__(self):
        self.reset()

    def reset(self):
        self.samplerate = None
        self.bitrate = 600000.0
        self.bits = []
        self.edges = []
        self.half_one = False
        self.start_one = 0
        self.UI_US = 1000000 / self.bitrate
        self.THRESHOLD_US = (self.UI_US + 2 * self.UI_US) / 2

    def metadata(self, key, value):
        if key == srd.SRD_CONF_SAMPLERATE:
            self.samplerate = value
            self.threshold = self.us2samples(self.THRESHOLD_US)

    def us2samples(self, us):
        return int(us * self.samplerate / 1000000)

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def decode(self):
        if not self.samplerate:
            raise SamplerateError('Cannot decode without samplerate.')
        while True:
            self.wait([{0: 'e'}])
            samplenum = self.samplenum
            if not self.edges:
                self.start_one = samplenum
                self.edges.append(samplenum)
                continue
            diff = samplenum - self.edges[-1]
            if diff > self.threshold:
                self.bits.append(0)
                self.put(self.edges[-1], samplenum, self.out_ann, [0, ['0']])
                self.half_one = False
                self.start_one = 0
            else:
                if self.half_one:
                    self.bits.append(1)
                    self.put(self.start_one, samplenum, self.out_ann, [1, ['1']])
                    self.half_one = False
                    self.start_one = 0
                else:
                    self.half_one = True
                    self.start_one = self.edges[-1]
            self.edges.append(samplenum)
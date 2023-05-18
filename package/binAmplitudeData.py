class BinAmplitudeData:
    def __init__(self, ch_center_freq, freq_span, num_of_bins, bin_spacing, resolution_bw, amplitude):
        self.ch_center_freq = ch_center_freq
        self.freq_span = freq_span
        self.num_of_bins = num_of_bins
        self.bin_spacing = bin_spacing
        self.resolution_bw = resolution_bw
        self.amplitude = amplitude

    def __str__(self):
        return f"BinAmplitudeData: ChCenterFreq={self.ch_center_freq}, FreqSpan={self.freq_span}, NumberOfBins={self.num_of_bins}, BinSpacing={self.bin_spacing}, ResolutionBW={self.resolution_bw}"

    @staticmethod
    def from_bytes(data_bytes):
        ch_center_freq = int.from_bytes(data_bytes[0:4], byteorder='big')
        freq_span = int.from_bytes(data_bytes[4:8], byteorder='big')
        num_of_bins = int.from_bytes(data_bytes[8:12], byteorder='big')
        bin_spacing = int.from_bytes(data_bytes[12:16], byteorder='big')
        resolution_bw = int.from_bytes(data_bytes[16:20], byteorder='big')
        amplitude = []
        for i in range(20, len(data_bytes), 2):
            amplitude.append(int.from_bytes(data_bytes[i:i+2], byteorder='big', signed=True))
        return BinAmplitudeData(ch_center_freq, freq_span, num_of_bins, bin_spacing, resolution_bw, amplitude)

    def to_bytes(self):
        data_bytes = bytearray()
        data_bytes.extend(self.ch_center_freq.to_bytes(4, byteorder='big'))
        data_bytes.extend(self.freq_span.to_bytes(4, byteorder='big'))
        data_bytes.extend(self.num_of_bins.to_bytes(4, byteorder='big'))
        data_bytes.extend(self.bin_spacing.to_bytes(4, byteorder='big'))
        data_bytes.extend(self.resolution_bw.to_bytes(4, byteorder='big'))
        for amp in self.amplitude:
            data_bytes.extend(amp.to_bytes(2, byteorder='big', signed=True))
        return data_bytes

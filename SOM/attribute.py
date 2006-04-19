class AttributeList(dict):
    def __init__(self):
        import instrument
        import sample
        self.instrument=instrument.Instrument()
        self.sample=sample.Sample()

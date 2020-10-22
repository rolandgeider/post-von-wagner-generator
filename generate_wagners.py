from textgenrnn import textgenrnn

t = textgenrnn('textgenrnn_weights.hdf5')
t.generate(20, temperature=0.4)
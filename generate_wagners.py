from textgenrnn import textgenrnn

"""
Generate Posts von Wagner for your reading pleasure.

The n parameter is the amount of texts the system should generate.

The temperature is the creativity the AI is allowed to show. At values close to
one, it will even invent words... Use values higher than one at your own risk
"""

t = textgenrnn('textgenrnn_weights.hdf5')
t.generate(n=20, temperature=0.6, max_gen_length=350)

# If you want to generate texts that begin with a specific phrase:
# t.generate(n=20, temperature=0.4, max_gen_length=700, prefix="Liebe Annete Schavan")
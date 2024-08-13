import sbol3

# Create a new document
doc = sbol3.Document()

# Create a ComponentDefinition
comp = ComponentDefinition('myComponent')

# Create a DNA sequence
seq = Sequence('mySequence', 'dna', 'ACTGACTG')

# Associate the sequence with the component
comp.sequences.append(seq)

# Add the component to the document
doc.addComponentDefinition(comp)

# Write the document to a file
doc.write('my_document.sbol3')
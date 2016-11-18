from odbAccess import*
from abaqusConstants import *
from odbMaterial import *
from odbSection import *
from textRepr import *
Path='C:\\Documents and Settings\\Arato\\Pulpit\\abaqus\\'
odbFile = Path+'S107-cr-1_law_of_mixture.odb'
odb = session.openOdb(odbFile, readOnly=True)

values = odb.steps.values()

valuesCount = len(values[0].frames[0].fieldOutputs['S'].values)
frameCount = len(values[0].frames)

for i in range(0, frameCount):
    name_output_file = "wyniki\\inkrement"
    fout = open(Path + name_output_file+str(i)+".txt", mode="w")
    for j in range(0,valuesCount):
        SValues = values[0].frames[i].fieldOutputs['S'].values[j].mises
        PEEQValues = values[0].frames[i].fieldOutputs['PEEQ'].values[j].data
        EVOLValues = values[0].frames[i].fieldOutputs['EVOL'].values[j].data
  #  RF_to_file = setValues[i].mises
        fout.write(str(i))
        fout.write(':')
        fout.write(str(j))
        fout.write(':')
        fout.write(str(SValues))
        fout.write(':')
        fout.write(str(PEEQValues))
        fout.write(':')
        fout.write(str(EVOLValues))
        fout.write('\n')
    fout.close()

odb.close()
from odbAccess import*
from abaqusConstants import *
from odbMaterial import *
from odbSection import *
from textRepr import *
Path='S:\\Abaqus Tmp\\'
odbFile = Path+'NEW_TET.odb'
odb = session.openOdb(odbFile, readOnly=True)

values = odb.steps.values()

valuesCount = len(values[0].frames[0].fieldOutputs['U'].values)
frameCount = len(values[0].frames)


for i in range(0,frameCount):
 name_output_file = "inkrement"
 fout = open(Path  +"NEW_TET\\"+name_output_file+str(i)+".txt", mode="w")
 S = values[0].frames[i].fieldOutputs['S']
 PEEQ = values[0].frames[i].fieldOutputs['PEEQ']
 EVOL = values[0].frames[i].fieldOutputs['EVOL']
 U = values[0].frames[i].fieldOutputs['U']
 for j in range(0,valuesCount):  #95622
  fout.write(str(i))
  fout.write(':')
  fout.write(str(S.values[j].elementLabel-1))
  fout.write(':')
  fout.write(str(U.values[j].data[0]))
  fout.write(':')
  fout.write(str(U.values[j].data[1]))
  fout.write(':')
  fout.write('\n')
 fout.close()

fout_materials = open(Path +"NEW_TET\\Materialy.txt", mode="w")
fout_materials.write(str(valuesCount))
fout_materials.write(':')
fout_materials.write(str(frameCount))
fout_materials.write('\n')
for j in range(0,valuesCount):
 fout_materials.write(str(j+1))
 fout_materials.write(':0')
 fout_materials.write('\n')
fout_materials.close()
odb.close()

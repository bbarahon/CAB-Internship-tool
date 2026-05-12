#*******************************
#      MADCUBA_STARS_tool
#*******************************
#Author: Borja Barahona Gómez
#Supervisors: Miguel Sanz Novo, Victor M. Rivilla Rodríguez.
#Description: this tool automatises the detection of molecules with different log(N) and the rest of parameters fixed. Then, if the detection succeeds, generates a simulated spectrum of the detected molecule and saves it in a single .c file. This tool also provides a cleaning system of files in order to obtain straightforward outputs.

print "************************"
print "STARTING SCRIPT"
print "************************"

from java.lang import Runtime
from java.util import Date
from java.text import SimpleDateFormat
from java.io import File,FileWriter,BufferedWriter
from ij import IJ
from ij.io import OpenDialog
datestart = Date()
print "START TIME"
print datestart

# 1. SETTING VARIABLES
Tex = 10 
FWHM =20 
vlos =0
FreqMin=30000
FreqMax=50000
wantrefs=1
j=0
inputFile ="/home/bbarahon/Descargas/INPUT_moleculardata_Barahona2026_sample.txt" #(CHANGE)
outputPath = "/home/bbarahon/Descargas/1.Synthetic_Spectra/1.All_MADCUBA_SYNTHETIC" #(CHANGE)
if File("%s" % outputPath).exists(): 
      carpetaantigua=File("%s" % outputPath)
      archivos=[f for f in carpetaantigua.listFiles() if f.isFile()]
      for archivo in archivos:
         archivo.delete();
      File("%s" % outputPath).delete()
cleanThreshold=1e-06
goodmolecules=[]
detectedmolecules=[]
catalogs=[]
logsN=[]
refs=[]
f = open(inputFile,'r')
firstMolecule = 1
for inputlines in f.readlines(): 
   if len(inputlines.split('/'))<3:
      continue 
   if "#" in inputlines:
      continue 
   molecule=inputlines.split('/')[0] 
   catalog= inputlines.split('/')[1] 
   logN= inputlines.split('/')[2] 
   ref=inputlines.split('/')[3] 
# 2. OPEN MADCUBA SPECTRA AND OTHERS
   if firstMolecule:   
      IJ.run("Open Spectra", "select='/home/bbarahon/Descargas/SAMPLESPECTRUM.spec'");  #(CHANGE)
      IJ.run("Select Tab", "nametab=SAMPLESPECTRUM.fits'");	
      IJ.run("Select Rows", "rows=1#2#");
      IJ.selectWindow("PLOT SAMPLESPECTRUM.fits|Orig."); #(CHANGE)
      firstMolecule= 0
   j+=1
   IJ.run("SLIM Search", " range='%s %s' axislabel='Frequency' axisunit='GHz' molecules='%s       $%s$Any$Any$Any$#' searchtype=new datafile='SAMPLESPECTRUM.fits|Orig.' datatype=SPECTRA" % (FreqMin,FreqMax,catalog,molecule)); #(CHANGE)
   IJ.run("SLIM Select Molecule", "molecule='%s' component=1 " % (molecule));
   IJ.run("SLIM Load Transition", "load"); 
   IJ.run("SLIM Select Rows", "indexrange=0 rows=ALL component=1#"); 
#3. SIMULATION
   IJ.run("SLIM SIMULATE", "molecules='%s|1#' logn=%s flogn=false tex=%s velo=%s fvelo=false fwhm=%s ffwhm=false sourcesize=0.0 fsourcesize=true continuum=false threshold=1.0E-4 typethreshold=intensity " %(molecule, logN, Tex, vlos, FWHM));
#4. SAVING
   IJ.run("SLIM SAVE SIMULATE ASCII", "component='ALL' xaxis='Rest Freq' molecules='%s' select='%s/%s'" %(molecule, outputPath, molecule));
    #-------------------------------------
   #CODE FOR DETECTING THE MOLECULE
   #-------------------------------------
   ruta="%s/%s" % (outputPath, molecule) 
   carpeta=File(ruta)
   if molecule=='C2H3NH2,0-<-0+':
      name='C2H3NH2'
      dest=File("%s/simulate_generate_%s" % (outputPath, name))
   else:
      dest=File("%s/simulate_generate_%s" % (outputPath, molecule))
   archivos=[f for f in carpeta.listFiles() if f.isFile()] 
   ficheros=carpeta.listFiles()
   writer=BufferedWriter(FileWriter(dest))
   FoundTransitions=[]
   AllTransitions=[]
   count=1
   for i in range(1,len(archivos)+1): 
      if File(ruta).exists(): 
         fcheck=open("%s/%s/simulate_generate_%s" % (outputPath, molecule, str(i)), "r") 
         lines=fcheck.readlines() 
         for k in lines: 
            parts=k.strip().split("\t") 
            if len(parts)==2: 
               Transitions=1 
               break 
            else:
               Transitions=0 
      else: 
         Transitions=0 
      FoundTransitions.append(Transitions)
      ceros=[0]*count
      count+=1
      if FoundTransitions==ceros:
         break
      AllTransitions.append(1)
      if j-1 not in goodmolecules:
         goodmolecules.append(j-1)
         detectedmolecules.append(molecule)
         catalogs.append(catalog)
         logsN.append(logN)
         refs.append(ref)
      for fichero in ficheros:
         if fichero.isFile() and fichero.getName().endswith("_%s" %str(i)):
            reader=BufferedReader(FileReader(fichero))
            linea=reader.readLine()
            if fichero.getName().endswith("_1"):
               writer.write(linea)  
               writer.newLine()
            while linea is not None:
               linea = reader.readLine()
               if linea is not None:  
                  writer.write(linea)
                  writer.newLine()
            reader.close()
            source=File("%s/%s/simulate_generate_%s" % (outputPath, molecule, str(i)))
            source.delete()
      ceros=[]
      FoundTransitions=[]
      count=1
   writer.close()
   File("%s/%s" % (outputPath, molecule)).delete()
   if len(AllTransitions)==0:
      if wantrefs==1:
         print '%s,%s,%s,%s' %(catalog,molecule,logN,ref) 
      elif wantrefs==0:
         print '%s,%s,%s' %(catalog,molecule,logN)
      else:
         print "ERROR: you have put a different value for wanting references!!"
         break
      print "WARNING: no transitions found for molecule %s (%s)" % (molecule, catalog)
      for p in range(1,len(archivos)+1):
         File("%s/%s/simulate_generate_%s" % (outputPath, molecule, str(p))).delete();
      File("%s/%s" % (outputPath, molecule)).delete()
      dest.delete()
      continue
   else:
      IJ.run("SLIM Get Spectrum", "molecules='%s|1#' sort='Intensity' lines='Mol.-sel' range=1.0E9 xaxis='Rest_Freq' " % molecule); 
      if wantrefs==1:
         print "Simulated the following molecule: '%s' from '%s' with log(N)=%s, Tex=%s, Vlos=%s and FWHM=%s. Reference: %s" %(molecule,catalog, logN, Tex, vlos,FWHM,ref) 
      elif wantrefs==0:
         print "Simulated the following molecule: '%s' from '%s' with log(N)=%s, Tex=%s, Vlos=%s and FWHM=%s." %(molecule, catalog, logN, Tex, vlos,FWHM)
      else:
         print "ERROR: you have put a different value for wanting references!!"
         break
   File("%s/%s/simulate_generate_%s" % (outputPath, molecule, str(i))).delete();
   File("%s/%s" % (outputPath, molecule)).delete();
   print "saved as:"
   print "'%s/simulate_generate_%s'" %(outputPath, molecule)
   count=1
print "Detected %s molecules from %s." % (len(goodmolecules), j)
print "Saving all data of detected molecules in %s" %outputPath
if File("%s/molecular_gooddata.txt" %outputPath).exists:
   fw=FileWriter("molecular_gooddata.txt");
   bw2=BufferedWriter(fw);
   bw2.write(" ");
   bw2.close();
   fw=FileWriter("%s/molecular_gooddata.txt" % outputPath,1);
   bw=BufferedWriter(fw);
   for k in range(len(goodmolecules)):
      if detectedmolecules[k]=='C2H3NH2,0-<-0+':
         name='C2H3NH2'
         bw.write("%s|%s|%s|%s" % (name,catalogs[k],logsN[k],refs[k]));
      else:
         bw.write("%s|%s|%s|%s" % (detectedmolecules[k],catalogs[k],logsN[k],refs[k]));
   bw.write("************************");
   bw.write("START TIME: ");
   bw.write("%s" % (datestart));
   bw.write(". END TIME: ");
   dateend = Date()  
   bw.write("%s" % (dateend));
   bw.write("************************");
   bw.close();
else:
   fw=FileWriter("%s/molecular_gooddata.txt" % outputPath,1);
   bw=BufferedWriter(fw);
   for k in range(len(goodmolecules)):
      bw.write("%s|%s|%s|%s" % (detectedmolecules[k],catalogs[k],logsN[k],refs[k]));
   bw.write("************************");
   bw.write("START TIME: ");
   bw.write("%s" % (datestart));
   bw.write(". END TIME: ");
   dateend = Date()  
   bw.write("%s" % (dateend));
   bw.write("************************");
   bw.close();
print "DONE"
print "************************"
print "START TIME"
print datestart
datestart = Date()  
print "END TIME"
print datestart

print "************************"

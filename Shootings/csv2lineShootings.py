#!/usr/bin/python
import sys, getopt
import progressbar
import time
import pandas as pd
import datetime

def main(argv):
   dbname = 'import'
   inputfile = 'data.csv'
   outputfile = 'import.txt'

   usage = 'csv2line.py -d <dbname> -i <inputfile> -o <outputfile>'
   try:
      opts, args = getopt.getopt(argv,"hd:i:o:",["db=","ifile=","ofile="])
   except getopt.GetoptError:
      print (usage)
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print (usage)
         sys.exit()
      elif opt in ("-d", "--db"):
         dbname = arg.replace(" ", "_")
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   convert(dbname, inputfile, outputfile)


def convert(dbname, inputfile, outputfile):
  # Convert csv's to line protocol
  '''
  https://docs.influxdata.com/influxdb/v1.6/write_protocols/line_protocol_tutorial/
  weather,location=us-midwest temperature=82 1465839830100400200
    |    -------------------- --------------  |
    |             |             |             |
    |             |             |             |
  +-----------+--------+-+---------+-+---------+
  |measurement|,tag_set| |field_set| |timestamp|
  +-----------+--------+-+---------+-+---------+
  '''
  start_time = time.time()
  
  # Read csv
  bar = progressbar.ProgressBar(maxval=100, widgets=[progressbar.Bar('=', '[', ']'), 'Read csv file ', progressbar.Percentage()])
  bar.start()
  df_full = pd.read_csv(inputfile)
  bar.finish()

  # Export to file
  theImportFile = open(outputfile, 'w')
  # Write header file
  theImportFile.write('''
# DDL
CREATE DATABASE %s

# DML
# CONTEXT-DATABASE: %s

''' % (dbname, dbname))

  # Measurement
  bar = progressbar.ProgressBar(maxval=len(df_full), widgets=[progressbar.Bar('=', '[', ']'), 'Processing ', progressbar.Percentage()])
  bar.start()
  	
  b = 0
  c = 0
  seen = {}
  l = 1
  for d in range(len(df_full)):
    
    bar.update(d+1)
    s = str(df_full["IncidentDate"][d])


    if l > 1:
	comp = str(df_full["IncidentDate"][d-1])
    else: 
	comp = str(df_full["IncidentDate"][d])

    l = l + 1

    if s == "nan":	
	#timestamp = time.mktime(datetime.datetime.strptime(s, "%m-%d-%Y %H:%M:%S").timetuple())
	timestamp = "00-00-0000 00:00:00"
    else:    
	if s == comp:

		if c < 10:
			if b < 10:
				s = s + " 00:00:0" + str(b)
    				timestamp = time.mktime(datetime.datetime.strptime(s, "%B %d, %Y %H:%M:%S").timetuple())
				c = c + 1
				b = b + 1
			elif b >= 10:
				s = s + " 00:00:" + str(b)
	                        timestamp = time.mktime(datetime.datetime.strptime(s, "%B %d, %Y %H:%M:%S").timetuple())
                        	c = c + 1
				b = b + 1
		elif c > 60:
			a = 1
			b = 0

			if b < 10:
				s = s + " 00:0" + str(a) + ":0" + str(b)
				timestamp = time.mktime(datetime.datetime.strptime(s, "%B %d, %Y %H:%M:%S").timetuple()) 			
			elif b >= 10:
				s = s + " 00:0" + str(a) + ":" + str(b)
                	        timestamp = time.mktime(datetime.datetime.strptime(s, "%B %d, %Y %H:%M:%S").timetuple())

			c = c + 1
			b = b + 1
		elif c > 120:
			a = 2
			b = 0

 			if b < 10:
                        	s = s + " 00:0" + str(a) + ":0" + str(b)
                        	timestamp = time.mktime(datetime.datetime.strptime(s, "%B %d, %Y %H:%M:%S").timetuple())
                        elif b >= 10:
                        	s = s + " 00:0" + str(a) + ":" + str(b)
                        	timestamp = time.mktime(datetime.datetime.strptime(s, "%B %d, %Y %H:%M:%S").timetuple())
			c = c + 1 
			b = b + 1		

		elif c > 180:
			a = 3
			b = 0

			if b < 10:
                                s = s + " 00:0" + str(a) + ":0" + str(b)
                                timestamp = time.mktime(datetime.datetime.strptime(s, "%B %d, %Y %H:%M:%S").timetuple())
                        elif b >= 10:
                                s = s + " 00:0" + str(a) + ":" + str(b)
                                timestamp = time.mktime(datetime.datetime.strptime(s, "%B %d, %Y %H:%M:%S").timetuple())
			c = c + 1
			b = b + 1	

		elif c > 240:

			a = 4
			b = 0
		
			if b < 10:
                                s = s + " 00:0" + str(a) + ":0" + str(b)
                                timestamp = time.mktime(datetime.datetime.strptime(s, "%B %d, %Y %H:%M:%S").timetuple())
                        elif b >= 10:
                                s = s + " 00:0" + str(a) + ":" + str(b)
                                timestamp = time.mktime(datetime.datetime.strptime(s, "%B %d, %Y %H:%M:%S").timetuple())
			c = c + 1
			b = b + 1
		l = l + 1

	else:
		s = str(df_full["IncidentDate"][d])
		timestamp = time.mktime(datetime.datetime.strptime(s, "%B %d, %Y").timetuple())
		c = 0
		#timestamp = "00-00-0000 00:00:00"

    lines = ["shooting "
            + "IncidentDate=\"" + str(df_full["IncidentDate"][d]) + "\","
            + "State=\"" + str(df_full["State"][d]).replace("\"","'") + "\","
            + "CityOrCounty=\"" + str(df_full["CityOrCounty"][d]) + "\","
            + "Address=\""+ str(df_full["Address"][d]) + "\","
            + "Killed=" + str(df_full["Killed"][d]) + ","
            + "Injured=" + str(df_full["Injured"][d]) + ","
            + "Operations=\"" + str(df_full["Operations"][d]) + "\""
	    + " " + str(timestamp).replace(".0", "")]

    l = l+1

    for item in lines:
	theImportFile.write("%s\n" % item)
    #if item in seen: continue
    #theImportFile.write("%s\n" % item)
    #seen[item] = 1

  bar.finish()

  # Print log
  print ('---Converting finished !!! (%s seconds)---' % (time.time() - start_time))
  print ('\t-Dabase name is: %s' % dbname)
  print ('\t-Input file is: %s' % inputfile)
  print ('\t-Output file is: %s' % outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])


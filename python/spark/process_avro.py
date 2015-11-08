import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import codecs
import json
import happybase

connection = happybase.Connection('10.1.94.57')
tab = connection.table('aaron_memex_ht-images')

#s=codecs.open("/Users/amandeep/ads-image-avro-schema.avsc",'r')
o=codecs.open("ads-image-mapping-input-for-karma",'w','utf-8')
reader = DataFileReader(open('/Users/amandeep/Downloads/part-m-00000-2.avro','r'),DatumReader())
for line in reader:
	#print line
	#print "images id:" + str(line["images_id"])
	rows = tab.rows(str(line["images_id"]))
	for row in rows:
		jsonO={}
		ads_url = line['ads_url']
		jsonO["ads_id"]=str(line["ads_id"])
		jsonO["columbia_near_dups"]=row[1]['meta:columbia_near_dups']
		jsonO["original_url"]=row[1]['meta:url']
		jsonO["columbia_near_dups_dist"]=row[1]['meta:columbia_near_dups_dist']
		jsonO["ads_url"]=ads_url
		jsonO["s3_url"]=row[1]['meta:location']
		jsonO["images_id"]=str(line['images_id'])

		o.write(ads_url + '\t' + json.dumps(jsonO))
		o.write('\n')
	

o.close()

	#print row[1]['meta:columbia_near_dups']#,row[1]["meta:columbia_near_dups"]
	#break
reader.close()

import os,sys

### Reads the existing crawl databases and adds them to the JEF config for monitoring
### There is no method in JEF to pass mutliple indexes at once.

def createDbXML(dbList):
    return '<monitored-paths>' + ''.join(['<path>' + db + "</path>" for db in dbList]) + '</monitored-paths>'

def constructXML(original,pathsXML):
    with open(original,'r') as originalXML:
        origStr = originalXML.read()
        with open(original.replace(".xml","-2.xml"),'w') as outputXML:
            outputXML.write(origStr.replace("<monitored-paths></monitored-paths>",pathsXML))

def get_crawldbs(crawldb_dir):
    return os.listdir(crawldb_dir)

def construct_databases(dbFile,parentDir,suffix=None):
    with open(dbFile,'r') as databaseFile:
        return [os.path.join(parentDir, db.replace("\n",""), suffix) for db in databaseFile.readlines()]

if __name__ == "__main__":
    suffix = "progress/latest"
    constructXML(sys.argv[1], createDbXML([os.path.join(sys.argv[2],db,suffix) for db in os.listdir(sys.argv[2])]))




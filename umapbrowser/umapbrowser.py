
from pathlib import Path
import json
import numpy as np
import gzip
import os
import codecs

def run(dataLabels, data2DPoints, outputDirectory, pageRoot, port=8421, webui=True):
    """
    Writes static html files needed to host umap browser, and then runs webui
    """
    pageRoot = str(pageRoot).replace("\\", "/")
    outputDirectory = str(outputDirectory).replace("\\", "/")
    outputDirectory = Path(outputDirectory)
    pageRoot = str(pageRoot)[:-1] if str(pageRoot).endswith("/") else str(pageRoot)
    pageRootNoFirst = str(pageRoot)[1:] if str(pageRoot).startswith("/") else str(pageRoot)
    rootDir = outputDirectory / pageRootNoFirst
    writeFiles(dataLabels=dataLabels, data2DPoints=data2DPoints, rootDir=rootDir, pageRoot=pageRoot)
    if webui:
        runWebui(path=rootDir, port=port)

def writeFiles(dataLabels, data2DPoints, rootDir, pageRoot): 
    """
    Writes the static html files needed to host umap browser to the rootDir, intended to be served under your website at pageRoot
    """
    rootDir.mkdir(parents=True, exist_ok=True)
    pointsBytes = np.array(data2DPoints).astype("<f4").tobytes()
    outputPointsPath = rootDir / "points.bin"
    htmlPointsPath = pageRoot + "/" +  "points.bin"
    with open(outputPointsPath, "wb") as f:
        f.write(pointsBytes)
    
    # map everything to single file for now, same index
    mappingFromDataToFiles = np.zeros([len(data2DPoints), 2])
    mappingFromDataToFiles[:,1] = np.arange(len(data2DPoints))
    
    dataMappingBytes = mappingFromDataToFiles.astype("<i4").tobytes()
    outputDataMappingPath = rootDir / "dataMapping.bin"
    htmlDataMappingPath = pageRoot + "/" + "dataMapping.bin"
    with open(outputDataMappingPath, "wb") as f:
        f.write(dataMappingBytes)
     
    dataDir = rootDir / "data"
    dataDir.mkdir(parents=True, exist_ok=True)
    dataHtmlRoot = pageRoot + "/" + "data"
    dataFile = dataDir / "data0.json.gz"
    with gzip.open(dataFile, "wt", encoding="utf-8") as gz:
        json.dump(dataLabels, gz, separators=(",", ":")) # specifying seperators like this makes it smaller by remove whitespace
     
    outputTemplatePath = rootDir / "index.html"
    pathContainingTemplate = os.path.dirname(os.path.abspath(__file__))
    with codecs.open(os.path.join(pathContainingTemplate, "umapBrowserTemplate.html"), "r", 'utf-8') as f:
        templateText = f.read()
    templateText = templateText.replace("POINTSFILEPATH", str(htmlPointsPath)) \
                               .replace("DATAMAPPINGFILEPATH", str(htmlDataMappingPath)) \
                               .replace("BASEDATAPATH", str(dataHtmlRoot))
    with codecs.open(outputTemplatePath, "w", 'utf-8') as f:
        f.write(templateText)
      
def runWebui(path, port):
    """
    Runs a simple http server at the given path, using the given port
    """
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=path, **kwargs)
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving at http://localhost:{port}")
        while True:
            httpd.timeout = 0.5          # seconds – how long handle_request() can block  
            httpd.handle_request()   # serves at most one request
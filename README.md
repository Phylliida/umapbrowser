# umapbrowser
Simple webui to explore runs of UMAP on text data

See outputs for what this looks like [here](https://www.phylliida.dev/modelwelfare/refusalvsbailv3/umap).

Right now word cloud and frequencies are buggy, will be fixed eventually (should be small fix).

## Installation

```
pip install git+https://github.com/Phylliida/UMAP-Browser
```

## Usage

```python
import umapbrowser

# text labels, of size N, for each of your data points
dataLabels = ['hi', 'this', 'this', 'is', 'a', 'label', 'for your data']

# np array of shape [N,2], these are outputs from your umap run
data2DPoints = ...

# The directory where static html file will be stored (will be created if does not exist)
outputDirectory = "umapwebui-output"

# Base url of your umap data (for webui)
pageRoot = "/umapwebui" 

# port of webui
port = 8421

# generate the html files and host webui
umapbrowser.run(dataLabels=dataLabels, data2DPoints=data2DPoints, outputDirectory=outputDirectory, pageRoot=pageRoot, port=port)

# you can pass webui=False to just generate the output files
```




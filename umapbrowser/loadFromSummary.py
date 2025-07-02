
import numpy as np
import umap
def getSummaryData():
    import json
    with open("summary.json", "rb") as f:
        summary = json.load(f)['models']
    
    modelLabels = []
    modelVectors = []
    # sort by model name so consistent order
    for model, modelData in sorted(list(summary.items()), key=lambda x: x[0]):
        modelLabels.append(model)
        curVec = np.array(modelData['rawBailPrArr'])
        mag = np.linalg.norm(curVec, ord=2)
        if mag == 0: mag = 1
        curVec /= mag
        modelVectors.append([x for x in curVec])
    modelVectors = np.array(modelVectors)
    umapModel = umap.UMAP(n_components=2, unique=True, verbose=True, metric='cosine')
    umapPoints = umapModel.fit_transform(modelVectors)
    return modelLabels, umapPoints
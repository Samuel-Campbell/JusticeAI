# -*- coding: utf-8 -*-
from sklearn.cluster import DBSCAN
import os
import numpy as np
import logging
logger = logging.getLogger('fact_clustering')


def clusterFacts(factDict):
    """
        Clusters all given facts using DBSCAN, and writes the resulting
        clusters into different files
        factDict: a Dictionary, where the keys are the sentence strings,
                  and the values are the associated sentence vectors
    """
    X = np.matrix(list(factDict.values()))
    ms = DBSCAN(min_samples=2, eps=0.4, n_jobs=-1)
    ms.fit(X)
    labels = ms.labels_
    n_clusters = len(np.unique(labels))
    logger.info("Number of estimated clusters : %d" % n_clusters)
    writeFactsToFile(factDict, labels)


def writeFactsToFile(factDict, labels):
    outputDirPath = r'cluster_dir'
    for i, sent in enumerate(factDict.keys()):
        filePath = os.path.join(outputDirPath, str(labels[i]))
        normalizedFilePath = os.path.normpath(filePath)
        f = open(normalizedFilePath + '.txt', 'a')
        f.write('{:.140}'.format(sent) + '\n')
        f.close()

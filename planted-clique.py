import igraph
import math
import random
import itertools
import heapq

from scale import doubler, adder

rootNLogN = lambda n: int(math.sqrt(n * math.log(n)))
justUnderRootN = lambda n: int(n**(0.5 - 0.05))


def addPlant(G, plantSize):
   numVertices = len(G.vs)
   plantVertices = list(range(plantSize))

   G.add_edges([(v,w) for v, w in itertools.combinations(plantVertices, 2) if not G.are_connected(v,w)])
   for i in range(numVertices):
      G.vs[i]['plant'] = True if i in plantVertices else False

   return G, plantVertices


def testPlantFindingAlgorithm(findPlant, vertexRange = None, getPlantSize = math.sqrt):
   if vertexRange is None:
      vertexRange = adder(200, 2000, 200)

   for n in vertexRange:
      numSuccesses = 0
      numTrialsPerN = 20

      for j in range(numTrialsPerN):
         G = igraph.Graph.Erdos_Renyi(n, 0.5)
         plantSize = int(getPlantSize(n))

         G, truePlant = addPlant(G, plantSize)
         outputtedVertices = findPlant(G, plantSize)

         if len(outputtedVertices) == plantSize and len([x for x in outputtedVertices if x['plant']]) == plantSize:
            numSuccesses += 1

      print("%d, %d: %G" % (n, plantSize, float(numSuccesses) / numTrialsPerN))


def deleteSmallestDegree(G, plantSize):
   while len(G.vs) > plantSize:
      degrees = dict(enumerate(G.degree()))
      vertexToDelete = min(G.vs, key=lambda v: degrees[v.index])
      G.delete_vertices([vertexToDelete.index])

   return G.vs


def batchDeleteSmallestDegree(G, plantSize):
   batchSize = plantSize

   while len(G.vs) > plantSize + batchSize:
      degrees = dict(enumerate(G.degree()))
      vsToRemove = heapq.nsmallest(batchSize, G.vs, key=lambda v: degrees[v.index])
      G.delete_vertices([v.index for v in vsToRemove])

   degrees = dict(enumerate(G.degree()))
   return heapq.nlargest(plantSize, G.vs, key=lambda v: degrees[v.index])


def deleteLargestDegree(G, plantSize):
   # delete the largest degree vertex which is whp not in the clique
   # if you cannot, stop and output highest plantSize many vertices

   thresholdAdditive = plantSize * math.sqrt(math.log(len(G.vs))) / 8
   def possiblyInClique(v, degrees):
      threshold = len(G.vs) / 2 + thresholdAdditive
      return (degrees[v.index] >= threshold and
         len([w for w in v.neighbors() if degrees[w.index] >= threshold]) >= threshold)


   while True:
      degrees = dict(enumerate(G.degree())) # dict of all vertex degrees
      notCliqueVertices = [v for v in G.vs if not possiblyInClique(v, degrees)]

      if len(notCliqueVertices) == 0:
         break
      else:
         vertexToDelete = min(G.vs, key=lambda v: degrees[v.index])

         if G.vs[vertexToDelete.index]['plant']:
            raise Exception("Deleting a plant vertex!")

         G.delete_vertices([vertexToDelete.index])

   print(len(G.vs))
   return heapq.nlargest(plantSize, G.vs, key=lambda v: degrees[v.index])


if __name__ == "__main__":
   # testPlantFindingAlgorithm(deleteSmallestDegree, getPlantSize = rootNLogN) # this should obviously work
   # testPlantFindingAlgorithm(deleteSmallestDegree) # definitely fails

   # testPlantFindingAlgorithm(batchDeleteSmallestDegree, getPlantSize = rootNLogN) # this should obviously work
   # testPlantFindingAlgorithm(batchDeleteSmallestDegree) # definitely fails

   #testPlantFindingAlgorithm(deleteLargestDegree, getPlantSize = rootNLogN) # this should obviously work
   # testPlantFindingAlgorithm(deleteLargestDegree, vertexRange=doubler(128, 16787), getPlantSize=justUnderRootN)
   testPlantFindingAlgorithm(deleteLargestDegree, vertexRange=doubler(256, 65536)) # fails, but close!
   pass

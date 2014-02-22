import igraph
import math
import random
import itertools
import heapq

from scale import doubler, adder

rootNLogN = lambda n: int(math.sqrt(n * math.log(n)))


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
   # delete the largest degree vertex which is definitely not in the clique
   # if you cannot, stop and output highest plantSize many vertices

   def possiblyInClique(v, degrees):
      return (degrees[v.index] >= plantSize and
         len([w for w in v.neighbors() if degrees[w.index] >= plantSize]) >= plantSize)


   while True:
      degrees = dict(enumerate(G.degree())) # dict of all vertex degrees
      notCliqueVertices = [v for v in G.vs if not possiblyInClique(v, degrees)]

      if len(notCliqueVertices) == 0:
         vertexToDelete = min(G.vs, key=lambda v: degrees[v.index])
         G.delete_vertices([vertexToDelete.index])
      else:
         break

   return heapq.nlargest(plantSize, G.vs, key=lambda v: degrees[v.index])


if __name__ == "__main__":
   # testPlantFindingAlgorithm(deleteSmallestDegree, getPlantSize = rootNLogN) # this should obviously work
   # testPlantFindingAlgorithm(deleteSmallestDegree) # definitely fails

   # testPlantFindingAlgorithm(batchDeleteSmallestDegree, getPlantSize = rootNLogN) # this should obviously work
   # testPlantFindingAlgorithm(batchDeleteSmallestDegree) # definitely fails

   #testPlantFindingAlgorithm(deleteLargestDegree, getPlantSize = rootNLogN) # this should obviously work
   #testPlantFindingAlgorithm(deleteLargestDegree) # definitely fails
   pass

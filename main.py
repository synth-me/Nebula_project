import Nebula
from Nebula import Nebula_root
from Nebula import Nebula_nlp
import nltk
from nltk.corpus import brown
from nltk.parse.generate import generate
from nltk import CFG
from nltk import Tree
import numpy as np

# those are the function that determines
# what each part of the genome will represent

nltk.download('brown')

n = []
v = []

b = brown.tagged_words()

counter = 0 
while counter < len(b):
  
  if b[counter][1] == 'NP':
    n.append(b[counter][0])
  
  if b[counter][1] == 'VB':
    v.append(b[counter][0])
    
  if len(v) and len(n) != 0:
    break
    pass 
    
  counter+=1


def rule1(b):
  return "SN -> '{subs[n_0]}' "
  
def rule2(b):
  return "SV -> '{subs[v_0]}' "
  
def rule3(b):
  return "SN1 -> '{subs[n_1]}' "

l = [
  rule1,
  rule2,
  rule3
  ]

ini = "S -> SN SV SN1"

subs = {
  'n_0':np.random.choice(n),
  'n_1':np.random.choice(n),
  'v_0':np.random.choice(v)
}

nomes = Nebula_root.init_label(500) 
genoma = Nebula_root.init_pop(500,3)
#g = Nebula_root.dna(nomes,genoma)
#a = Nebula_root.attr_by_position(len(genoma[0]),l)
#p = Nebula_nlp.process_teste(a,g)
#q = Nebula_nlp.grammar_extraction(p,ini,zz)
#s = Nebula_nlp.generate_sentence(q)
#t = Nebula_nlp.testing(s,g,'test',0.1)

i = Nebula_nlp.grammar_iteration(
  nomes,
  genoma,
  l,
  100,
  "testando o sistema",
  "S -> SN SV SN1",
  0,
  0.90,
  subs 
  )
Nebula_nlp.otimizatd_generation(i,0.80)


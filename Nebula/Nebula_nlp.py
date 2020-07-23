import Nebula
from Nebula import Nebula_root
import nltk
from nltk import CFG
from nltk.parse.generate import generate
from nltk.corpus import brown
import matplotlib.pyplot as plt
import random, string
import difflib
import colorama
from colorama import Fore
import numpy as np
from nltk import Tree
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget
import matplotlib.patches as mpatches


def grammar_extraction(population_g,inital_state,subs):

  population_s = {}
  
  for pop in population_g:
    p = [inital_state]
    
    for n in population_g[pop]:
      
      if n != 0:
        p.append(n)
        
      else:
        pass
        
    separ = "\n"
    prime_grammar = separ.join(p)
    pre_grammar = prime_grammar.format(subs=subs)
    
    pos_grammar = """
    {seed}
    """.format(seed=prime_grammar)
    
    post_grammar = """
    {seed}
    """.format(seed=pre_grammar)
    grammar_use = CFG.fromstring(post_grammar)
    
    population_s[pop] = (grammar_use,pos_grammar)
    
  return population_s


def generate_sentence(population_s):

	# here we will create a pool of sentences that will be
	# shown to the public and avaliated to return a feedback

	table = []
  
	for ps in population_s:
  
		grammar = population_s[ps][0]
		sent_cache = []
      
		for sentence in generate(grammar,n=2):
      
			sent = (ps, " ".join(sentence))
			sent_cache.append(sent)
			
		n = np.random.randint(len(sent_cache))
		sent_f = sent_cache[n]
		
		table.append(sent_f)
	
	return table


def testing(table, population_g,target,barrier):

	# here we test the sentences geenrated
	# if the sentences are well formed
	# it is out of the table list, otherwise they keep in the list
	# and are retired next
  counting = []
  counting_error = []
  package = []
  counter = 0
  while counter < len(table):
    
    sent_storage = []
    
    s = table[counter][1]
    sent_storage.append(s)
    
  
    similarity = difflib.SequenceMatcher(
    None, s, target).ratio()
    
    if similarity <= barrier:
      counting.append(similarity)
      table.remove(table[counter])
    else:
      print(Fore.RESET)
      counting_error.append(similarity)
      print(Fore.GREEN+str((round((similarity*100),2)))+'%')
      print(Fore.RESET)
      
    counter += 1
      
  for i in table:
    search_obj = i[0]
    if i[0] in population_g:
      population_g.pop(i[0])
    else:
      pass
  try:
    counting = sum(counting)/len(counting)
  except ZeroDivisionError:
    counting = 0
  
  try:
    counting_error = sum(counting_error)/len(counting_error)
  except ZeroDivisionError:
    counting_error = 0
    
  package.append(counting)
  package.append(population_g)
  package.append(counting_error)
  package.append(sent_storage)
  return package


def process_teste(a, genome):
  
	# here the genome is processed using the functions

	population_g = {}
  
	for i in genome:
		i_aux = {}
		v = []
# here we are gonna make a copy of genome
# so that we cant fall into the binary 
# position problem 
		
		counter = 0 
		for b in genome[i]:
		  
		  i_aux[counter] = b
		  counter+=1
		
		for k in i_aux:
		  v.append(a[k](i_aux[k]))		  
		
		population_g[i] = v 
		
	return population_g


def grammar_iteration(labels,genome,functions,rounds,target,inital_state,barrier,maximum_stop,subs):
  
  package_length = []
  
  length_list = []
  error_list = []
  otimization_list = []
# here we compile all functions based on Nebula_root 
# here we use the first paramters such as labels and genome
  g = Nebula_root.dna(labels,genome)
  a = Nebula_root.attr_by_position(len(genome[0]),functions)
  
# here we iterate it after rounds of iterations defined on parameters
  counter = 0
  while counter < rounds :
    
    pr = process_teste(a,g)
    
    q = grammar_extraction(pr,inital_state,subs)
    
    gs = generate_sentence(q)
    
    test = testing(gs,g,target,barrier)
    
    test_crossed = Nebula_root.transverse_crossover(test[1])
    test_in = Nebula_root.innovation(test_crossed)
    
# after each round of test we store the generation length 
    gen = (counter,len(test_in))
    if gen[1] == 0:
      break
      pass
    
    length_list.append(gen)
    
# here we store the error rate by getting the answers
    error_gen = (counter,test[2])
    error_list.append(error_gen)
    
    if test[2] >= maximum_stop or test[2] == 0:
      
      error_list.remove(error_gen)
      
      #parser = nltk.ChartParser(q)
      
      #cf = CanvasFrame()
      #t = Tree.fromstring(str(tree))
      #tc = TreeWidget(cf.canvas(),t)
      #cf.add_widget(tc,10,10)
      
      break
      pass
    
    
# here we store the otimization rate 
    otm_gen = (counter,test[0])
    otimization_list.append(otm_gen) 
    
    g = test_in
    print("//// Next generation ////")
    counter+=1
  
  package_length.append(length_list)
  package_length.append(error_list)
  package_length.append(otimization_list)
  
  return package_length
    
def otimizatd_generation(length_list,maximum_stop):
  
  plt.figure(figsize=(8,4))
# here we plot the length of each population   
  plt.subplot(131)
  plt.grid(True)
  plt.ylabel("Size/error/otimization")
  plt.xlabel("Generation")
  for l in length_list[0]:
    plt.scatter(l[0],l[1],color="blue")
  p_t = mpatches.Patch(color='blue',label='population size')
  plt.legend(handles=[p_t])
  
# here we plot the error rating  
  plt.subplot(132)
  plt.grid(True)
  plt.ylabel("") 
  plt.xlabel("Generation")
  plt.ylim([0,1])
  for l_2 in length_list[2]:
    plt.scatter(l_2[0],l_2[1],color="red")
  er = mpatches.Patch(color='red',label='erro rate')
  plt.legend(handles=[er])
  
  # here we plot the error rate
  plt.subplot(133)
  plt.grid(True)
  plt.ylabel("")
  plt.xlabel("Generation")
  plt.ylim([0,1])
  for l_3 in length_list[1]:
    if l_3[1] < maximum_stop :
      c = 'green'
    else:
      c = 'magenta'
    
    plt.scatter(l_3[0],l_3[1],color=c,label='teste')
  limit_1 = mpatches.Patch(color='green',label='less than max')
  limit_2 = mpatches.Patch(color='magenta',label='more than max') 
  
  plt.legend(handles=[limit_1,limit_2],loc='lower left')
  
  plt.suptitle("Optimization plot")
  plt.show()

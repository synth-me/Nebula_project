import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def inform_me():
  
  info = """
  That library was made as a simple genetic algorithm framework. That system was made by @AestheticGreek.
  
  This system was first desgined to be used as a framework to optmize probabilistic context-free grammars but it’s being upgraded to be able to optimze other domains.
  
  Wanna contact us? @murielpanegassi1@gmail.com
  
  """
  
  return info
  
def init_pop(total_length,genome_length):

# that attribute will create a radnom population
# of binary genomes  
  
  genome = []
  
  v = [0,1]
  
  counter = 0
  while counter < total_length :
    
    gn = []
    
    sub_counter = 0
    while sub_counter < genome_length :
      
      binary = np.random.choice(v)
      
      gn.append(binary)
      
      sub_counter+=1
    
    genome.append(gn)
    
    counter+=1 
    
  return genome  

def init_label(total_length):
  
  labels = [] 
  
  counter = 0
  while counter < total_length:
    
    import random, string
    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    labels.append(str(x))
     
    counter+=1
  return labels

def dna(labels, b_genome):

	genome = {}

	# here we will make a genome with given labels
	# and use a binary vector for each label

	# here we will connect each binary vector to a layer
	counter = 0
	while counter < len(labels):

		genome[labels[counter]] = b_genome[counter]

		counter += 1

	return genome


def attr_by_position(genome_length, genome):

	# here we attribute a function for each position of the
	# genome and we will store teh position in a dict

	attr_list = {}

	counter = 0
	while counter < genome_length:

		attr_list[counter] = genome[counter]

		counter += 1

	return attr_list


def crossover(dna_filtered):

	# the length must be  pair in order to create equal offsprings

	if len(dna_filtered) % 2 == 0:

		parents_combination = {}

		counter = 1
		while counter < len(list(dna_filtered.keys())):

			merged_half = [] 
			parent_1 = counter - 1
			parent_2 = counter
			p = (parent_1, parent_2)

			# here we find the pairs and crossover through sequencial elements
			# the crossove is done through half of each genome

			l1 = list(dna_filtered.keys())[counter]
			ld_1 = dna_filtered[l1]

			l2 = list(dna_filtered.keys())[counter - 1]
			ld_2 = dna_filtered[l2]

			# here we will test how the genme shuld be dividede
			# depeding on the length of the genome

			if len(ld_1) % 2 == 0 and len(ld_1) % 2 == 0:

				half_1 = ld_1[:int(len(ld_1) / 2)]

			elif len(ld_1) % 3 == 0 and len(ld_1) % 3 == 0:

				half_1 = ld_1[:int(len(ld_1) / 3)]

			if len(ld_2) % 2 == 0 and len(ld_2) % 2 == 0:

				half_2 = ld_2[:int(len(ld_2) / 2)]

			elif len(ld_2) % 3 == 0 and len(ld_2) % 3 == 0:

				half_2 = ld_2[:int(len(ld_2) / 3)]

	# here we store the values to merge the two parts

			for element_1 in half_1:
				merged_half.append(element_1)

			for element_2 in half_2:
				merged_half.append(element_2)

    
# it can be divided by three or two
# here we combine each half of the genomes
      
			parents_combination[p] = merged_half
  
			counter += 2
			
		return parents_combination

	else:
		return "the filtered dna should have a pair length"

def transverse_crossover(genome):
  
  storage_1 = []
  storage_2 = []
  
  parents_combination = {}
  
  counter = 0
  while counter < len(list(genome.keys())):
    
    g_k = list(genome.keys())[counter]
    g_c = genome[g_k]
    
    first_half = g_c[:int(len(g_c)/2)]
    storage_1.append(first_half)
    
    second_half = g_c[int(len(g_c)/2):]
    storage_2.append(second_half)
    
    counter+=1 
  
  storage_2.reverse()
  
  counter = 0 
  while counter < len(storage_2):
    
    parents_combination[counter] = []
    
    for b_2 in storage_2[counter]:
      
      parents_combination[counter].append(b_2) 
    
    for b_1 in storage_1[counter]:
      
      parents_combination[counter].append(b_1)
    
    counter+=1
    
  return parents_combination


def processing(atribute_by_position, genomes):

	# here the sysem execute the functions by the positon
	# defined through the attr_by_position
	# then it execute the sequenclicly the functions

	results = {}

	for genes in genomes:

		v = []
		vector = genomes[genes]

		for b in vector:
			v.append(atribute_by_position[b]())

		results[genes] = v

	return results


def innovation(population):
  
  aux_list = []
  
	# the function will find a rnadom position in the genome
	# then it will randomly substitute this position by a different binary
	# and of course it will make a change in the final content
	# this is necessary to generate variability in the offsprings
  
  for p in population.keys():
    
    v = population[p]
    genome_length = len(v)
    r_position = np.random.randint(genome_length)
    
    sub = v[r_position]
    v.remove(sub)
    
    if sub == 0:
      
      b = 1
      
    else:
      
      b = 0
    try:
      
      v.insert(v.index(sub), b)
      
    except ValueError:
      
      v.insert(0, b)
      
  return population


def selector(population_p, population_g):

	n_population = {}
	counter = []
	counter_sub = []

	# this will select through an selector the values in the population’s
	# and then exclude the the individuals with no fitiing

	for p in list(population_p.keys()):

		v = population_p[p].count(True)
		n_population[p] = v

	for n_p in n_population:

		selc = (n_p, n_population[n_p])
		counter_sub.append(n_population[n_p])
		counter.append(selc)
	
	# here the sysem wil exclude baseade on the 
	# lentgh of the population, if pair exclude two
	# if non-pair exlcude only one
		
	if len(list(population_g.keys())) %2 == 0:
	  
	  
	  out = min(counter_sub)
	  out_ind = counter_sub.index(out)
	    
	    
	  element_1 = counter[out_ind][0]
	  
	  population_p.pop(element_1)
	  population_g.pop(element_1)
	  
	  counter_sub.remove(out)
	  
	  out_2 = min(counter_sub)
	  out_2_ind = counter_sub.index(out_2)
	  
	  element_2 = counter[out_2_ind][0]
	  
	  try:
	    population_p.pop(element_2)
	    population_g.pop(element_2)
	  except:
	    pass 
	  
	else:
	  
	  out = min(counter_sub)
	  out_ind = counter_sub.index(out)
	  
	  element = counter[out_ind][0]
	  population_p.pop(element)
	  population_g.pop(element)

# if you wanna use a custom selector:
# the return have to be a dict, with the same length
# of each genome and the length of the dict have to be 
# smaller than the initial paramter 

	return population_g
  
	#  here we will make all info to use and execute #

def genetic_panda(list_1, list_2, list_3):

	# here we will input the results in a sheet
	# starting bthe initial pop , passing through the selected
	# and finishing with the mutate offspring

	data = {
	    "First pop": list_1,
	    "Selected pop": list_2,
	    "OffSpring": list_3,
	}

	gap_1 = len(list_1) - len(list_2)
	gap_2 = len(list_1) - len(list_3)

	counter = 0
	while counter < gap_1:
		list_2.append("R.I.P")
		counter += 1

	counter = 0
	while counter < gap_2:
		list_3.append("R.I.P")
		counter += 1

	df = pd.DataFrame(data)
	return df

def filogentic_tree(evolutionary_sheet):

# here we are will plot the result evolution 
# in a evolutionary tree that wil show
# the generations and the offsprings
  
  layer_1 = []
  layer_2 = []
  layer_3 = []
  
  storage_1 = []
  
  counter = 0 
  while counter < len(evolutionary_sheet.index):
    
    node = []
    
    n = evolutionary_sheet.iloc[counter]
    
    sub_counter = 0
    while sub_counter < 3 :
      
      p = (counter,sub_counter)
            
      node.append(p)
      
      if type(n[sub_counter]) is list :
        c = "blue"
      else:
        c = "red"
      
      plt.scatter(p[1],p[0],color=c)
      plt.plot(p[1],p[0])
      
      sub_counter+=1 
        
    storage_1.append(node)
    
    counter+=1
  
  plt.title("Evolution tree")
  plt.xlabel("Time")
  plt.ylabel("Generation")
  plt.show()
  
  return storage_1

def iteration(genome,labels,functions,rounds,dataframe=0,tree=0,custom=None,custom_p=None):

# here we simplify the use of the library by putting all
# steps of use together in the right way 

  counter = 0
  while counter < rounds :
    
    fp = []
    sp = []
    os = []
    
    offsprings = genome
    for g in offsprings:
      fp.append(offsprings[g])
    
    for egg in offsprings :
      a = attr_by_position(len(offsprings[egg]),functions)
    
    if custom_p == None:
      p = processing(a,offsprings)  
    else:
      p = custom(a,offsprings)
# here you can use a custom selector intead of the  
# binary one that is the deafult 
# to create a custom selctor follow the patterns 
# on the selector’s documentation

    if custom == None:
      s = selector(p,offsprings)
      for s_k in s:
        sp.append(s[s_k])
    else:
      s = custom(p,offsprings)
      for s_k in s:
        sp.append(s[s_k])
    
    c = transverse_crossover(s)
    
    genome = innovation(c)
    for i_k in genome :
      os.append(genome[i_k])
    
    evolutionary_sheet = genetic_panda(fp,sp,os)
    
    if dataframe == 0:
      pass 
    else:
      print("////////")
      print("Running "+str(counter)+" iteration...")
      print(evolutionary_sheet)
      print("////////")
    
  if tree == 0:
    pass
  else:
    filogentic_tree(evolutionary_sheet)
    
    counter+=1 
  return genome


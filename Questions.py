def get_question(n, t):
  return a[n][t]

a = [[0 for i in range(10)] for i in range(2)]

# a[i][j] = ["question", "option A", "option B", "option C", "option D", "correct answer"]

# Easy questions for the first part
a[0][0] = ["What is the color of the white horse of Henry the IV?","Blue","Brown","White","He didn't have a horse","White"]
a[0][1] = ["How do you say 'bread' in french?","baguette","pain","patate","bruchetta","pain"]
a[0][2] = ["What does WTH mean?","What The Hell","Wait The Humus","Why This Hair","Who Is Hannibal","What The Hell"]
a[0][3] = ["In which one of this Disney there is no love story (finally!)?","Frozen","Moana","Rapunzel","Aladdin","Moana"]
a[0][4] = ["In which color the logo 'Barbie' is written?","Salmon","Rose","Flamingo","Peach","Rose"]
a[0][5] = ["What is the name of the part of the human skeleton which protects our brain? ","tibia","arm","skull","toe","skull"]
a[0][6] = ["What can you buy in a butcher's shop?","meat","dress","television","iphone","meat"]
a[0][7] = ["On which continent is Peru located?","South-America","North-America","Europe","Africa","South-America"]
a[0][8] = ["What is the most populated country in the world?","Israel","UK","USA","China","China"]
a[0][9] = ["How many years are there in a millennium?","1","1000","10","100","1000"]

# Hard questions for the chase part
a[1][0] = ["Which GPU you need to use CUDA?","Intel Xe Graphics","NVIDIA","AMD","WTH?!","NVIDIA"]
a[1][1] = ["What is the real name of Manny in the movie Ice Age?","Manaudou","Manfred","Merlin","Manny","Manfred"]
a[1][2] = ["Sir Arthur Conan Doyle was a...?","Doctor","Policeman","Investigator","Bartender","Doctor"]
a[1][3] = ["How are called the mouthpart of spiders?","Ricinulei","Tetrapulmonata","Chelicerae","Needle","Chelicerae"]
a[1][4] = ["Who compose 'The Four Seasons'?","Beethoven","Stravinsky","Tchaikovsky","Vivaldi","Vivaldi"]
a[1][5] = ["Electric resistance is typically measured in what units?","litre","ohms","kg","km","ohms"]
a[1][6] = ["In which mountain range is Mount Everest?","Jura","Alpes","Vosges","himalaya","himalaya"]
a[1][7] = ["Who invented the telephone?","Alexandre Bell","Thomas Edison","Raffaele Esposito","Alexander Fleming","Alexandre Bell"]
a[1][8] = ["When did San Francisco earthquake happen?","1998","1906","2000","2006","1906"]
a[1][9] = ["How do you recognize a left-handed elephant?","He writes with his left hand","His left tusk is more used","He blinks with his left eye","He sleeps more on his right side","His left tusk is more used"]


def get_answer(n,t):
  q = get_question(n,t)
  return q[5]


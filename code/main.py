#!/usr/bin/env python
# coding: utf-8

# # Data manipulication
# This step is to get a 

# In[1]:


import pandas as pd


# In[2]:


#import data and merge Total population into this dataframe
df=pd.read_csv("./data/carbirth.csv",header=None)
df.set_axis(["State","Year" , "zero", "one",  "1orMore","twoorMore","threeorMore","fourorMore","BirthRate"],axis=1,inplace=True)
df2=pd.read_csv("./data/birthrate.txt",sep='\t')
df2=df2[['Year','State','TotalPopulation']].dropna()
df=df.merge(df2,on=['Year','State'])
df.head()


# In[3]:


ta=pd.read_csv('./data/tourist_attractions.csv')
ta=ta.drop('Unnamed: 0',axis=1)
ta.head()


# In[4]:


# group the DataFrame by column State
df_grouped = ta.groupby('State')

# create a dictionary with column State as the keys and the values in column Name as a list
tourists_dictionary = df_grouped['Name'].apply(list).to_dict()


# ## Create a data structure to store those information

# In[5]:


class StateData:
    def __init__(self,year,state,zero,one,oneorMore,twoorMore,threeorMore,fourorMore,BirthRate,TotalPopulation,tourist_attraction_list):
        self.year = year
        self.state = state
        self.zero=zero 
        self.one=one 
        self.oneorMore=oneorMore
        self.twoorMore=twoorMore
        self.threeorMore=threeorMore
        self.fourorMore=fourorMore
        self.BirthRate=BirthRate
        self.TotalPopulation=TotalPopulation
        self.tourist_attraction_list=tourist_attraction_list
        self.ta_number=len(tourist_attraction_list) if tourist_attraction_list!=None else 0
            

    def info(self):
        rep = '"' + '","'.join([str(self.year), self.state]) + '"\n'    
        return rep


# In[6]:


#create instances for those attributes
def get_statedata_instance():
    statedataList=[]
    for index, row in df.iterrows():
        year=row['Year']
        state=row['State']
        zero=row['zero']
        one=row['one']
        oneorMore=row['1orMore']
        twoorMore=row['twoorMore']
        threeorMore=row['threeorMore']
        fourorMore=row['fourorMore']
        BirthRate=row['BirthRate']
        TotalPopulation=row['TotalPopulation']
        tourist_attraction_list=tourists_dictionary[state] if state in tourists_dictionary else None

        touristsite = StateData(year,state,zero,one,oneorMore,twoorMore,threeorMore,fourorMore,BirthRate,TotalPopulation,tourist_attraction_list)
        statedataList.append(touristsite)
    return statedataList


# In[7]:


statedataList=get_statedata_instance()


# In[41]:


valid_state=[]
for inst in statedataList:
    if inst.state not in valid_state:
        valid_state.append(inst.state)


# # Define  a tree to store these data structures 

# In[8]:


class TreeNode:
    def __init__(self, year, state, zero, one, oneorMore, twoorMore, threeorMore, fourorMore, BirthRate, TotalPopulation, tourist_attraction_list, ta_number, children=[]):
        self.year = year
        self.state = state
        self.zero = zero
        self.one = one
        self.oneorMore = oneorMore
        self.twoorMore = twoorMore
        self.threeorMore = threeorMore
        self.fourorMore = fourorMore
        self.BirthRate = BirthRate
        self.TotalPopulation = TotalPopulation
        self.tourist_attraction_list = tourist_attraction_list
        self.ta_number = ta_number
        self.children = children
tree_node={}# create a dictinoary to store the tree nodes
# create a list of tree nodes
tree_nodes = []

# iterate over the statedataList
for statedata in statedataList:
    # create a new tree node for the current state data
    node = TreeNode(statedata.year, statedata.state, statedata.zero, statedata.one, statedata.oneorMore, statedata.twoorMore, statedata.threeorMore, statedata.fourorMore, statedata.BirthRate, statedata.TotalPopulation, statedata.tourist_attraction_list, statedata.ta_number)
    
    # add the new tree node to the list of tree nodes
    tree_nodes.append(node)


# iterate over the tree nodes
for node in tree_nodes:
    # if the current node's year is not a key in the tree_node dictionary, add it as a key and set its value to an empty list
    if node.year not in tree_node:
        tree_node[node.year] = []
    # add the current node to the list of child nodes for the current year
    tree_node[node.year].append(node)




# In[71]:


# import json

# # convert the tree_nodes data structure to a JSON object
# json_data = json.dumps(tree_nodes, default=lambda x: x.__dict__)

# # write the JSON object to a file
# with open('./tree_structure.json', 'w') as outfile:
#     json.dump(json_data, outfile)


# In[73]:


# define a function to print the data for a given year and state
def print_data(year, state):
    # look up the tree node for the given year and state
    nodelist = tree_node[year]

    for n in nodelist:
        if n.state==state:
            node=n
            
    
    # print the data for the tree node
    print(f"Year: {node.year}")
    print(f"State: {node.state}")
    print(f"Family with zero cars ownership rate: {node.zero}")
    print(f"Family with one car ownership rate: {node.one}")
    print(f"Family with one or more cars ownership rate: {node.oneorMore}")
    print(f"Family with two or more cars ownership rate: {node.twoorMore}")
    print(f"Family with three or more cars ownership rate: {node.threeorMore}")
    print(f"Family with four or more cars ownership rate: {node.fourorMore}")
    print(f"BirthRate: {node.BirthRate}")
    print(f"TotalPopulation: {node.TotalPopulation}")
#     print(f"tourist_attraction_list: {node.tourist_attraction_list}")
    print(f"Total tourist attraction number: {node.ta_number}")


# In[10]:


# print_data(2014, "California")
def yes(prompt):
    '''
    Answer a yes or no question.
    '''
    answer=["y", "yup", "yes","sure"]
    i=input(prompt)
    if i.lower() in answer:
        return True
    else:
        return False


# In[46]:


def get_attributes(state, y,attributes):
    # iterate over the tree_nodes or tree_node dictionaries

    for year, nodes in tree_node.items():
        for node in nodes:
            # if the current node has the given state, retrieve the specified attributes from the node
            if node.state == state and node.year == y:
                # retrieve the specified attributes from the TreeNode or StateData object
                values = [getattr(node, attr) for attr in attributes]
               
                # return the values of the specified attributes for the given state
                return values
    return False


# In[64]:


# define a function to print tourist attractions state
def print_tourist_attraction(state):
    # look up the tree node for the given  state


    for n in tree_nodes:
        if n.state==state:
            node=n
            
    print(f"Total rourist attraction number: {node.ta_number}")
    talist=node.tourist_attraction_list
    for ta in talist:
        print(f" {ta}")



# In[74]:


def user_options():
  print("Enter 1 to display an specific data for a state of a certain year")
  print("Enter 2 to get maximum/min value of a kind of data of all periods")
  print("Enter 3 to display all the attractions of a state")
  print("Enter 4 to enter a year, return this year's  maximum/min value and which state it is")
  option = input()
  
  if option == "1":
    while True:
        try:
            state = input("Enter the name of the state: ")
            if state in valid_state:
                break
            else:
                 print("Invalid state. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a  state.")
    while True:
        try:
            year = int(input("Enter a year between 2009 and 2017: "))
            if 2009 <= year <= 2017:
            # Year is valid, so we can exit the loop
                break
            else:
                print("Invalid year. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a numeric year.")
    printall=yes('Do you want to print all the values?')
    if printall:
        return print_data(year, state)
    attributes = ['year', 'state']
    if(yes('Do you want to print family with zero cars ownership rate ?')):
        attributes.append('zero')
    if(yes('Do you want to print family with one car ownership rate ?')):
        attributes.append('one')
    if(yes('Do you want to print family with one or more cars ownership rate ?')):
        attributes.append('oneorMore')
    if(yes('Do you want to print family with two or more cars ownership rate ?')):
        attributes.append('twoorMore')
    if(yes('Do you want to print family with three or more cars ownership rate ?')):
        attributes.append('threeorMore')
    if(yes('Do you want to print family with four or more ownership rate ?')):
        attributes.append('fourorMore')
    if(yes('Do you want to print BirthRate ?')):
        attributes.append('BirthRate')
    if(yes('Do you want to print TotalPopulation ?')):
        attributes.append('TotalPopulation')
    valuess = get_attributes(state,year, attributes)
    if valuess!=False:
            # print the values of the attributes
        print(valuess)
    else:
        print('Invalid data')
    return valuess
        
  elif option == "2":
    while True:
        if(yes('Do you  want to find the maximum/minimum value of family with zero cars ownership rate ?')):
            
            node_with_max = max(tree_nodes, key=lambda node: node.zero)
            node_with_min = min(tree_nodes, key=lambda node: node.zero)
            print("Minimum value:", node_with_min.zero,'State:',node_with_min.state,'Year:',node_with_min.year)
            print("Maximum value:", node_with_max.zero,'State:',node_with_max.state,'Year:',node_with_max.year)
            break

        if(yes('Do you want to find the maximum/minimum value of  family with one car ownership rate ?')):
            
            node_with_max = max(tree_nodes, key=lambda node: node.one)
            node_with_min = min(tree_nodes, key=lambda node: node.one)
            print("Minimum value:", node_with_min.one,'State:',node_with_min.state,'Year:',node_with_min.year)
            print("Maximum value:", node_with_max.one,'State:',node_with_max.state,'Year:',node_with_max.year)
            break
        if(yes('Do you want to print family with one or more cars ownership rate ?')):
            kind='oneorMore'
            node_with_max = max(tree_nodes, key=lambda node: node.oneorMore)
            node_with_min = min(tree_nodes, key=lambda node: node.oneorMore)
            print("Minimum value:", node_with_min.oneorMore,'State:',node_with_min.state,'Year:',node_with_min.year)
            print("Maximum value:", node_with_max.oneorMore,'State:',node_with_max.state,'Year:',node_with_max.year)
            break
            
        if(yes('Do you want to find the maximum/minimum value of  family with two or more cars ownership rate ?')):
            kind='twoorMore'
            node_with_max = max(tree_nodes, key=lambda node: node.twoorMore)
            node_with_min = min(tree_nodes, key=lambda node: node.twoorMore)
            print("Minimum value:", node_with_min.twoorMore,'State:',node_with_min.state,'Year:',node_with_min.year)
            print("Maximum value:", node_with_max.twoorMore,'State:',node_with_max.state,'Year:',node_with_max.year)
            break
            break
        if(yes('Do you want to find the maximum/minimum value of  family with three or more cars ownership rate ?')):
            kind='threeorMore'
            node_with_max = max(tree_nodes, key=lambda node: node.threeorMore)
            node_with_min = min(tree_nodes, key=lambda node: node.threeorMore)
            print("Minimum value:", node_with_min.threeorMore,'State:',node_with_min.state,'Year:',node_with_min.year)
            print("Maximum value:", node_with_max.threeorMore,'State:',node_with_max.state,'Year:',node_with_max.year)
            break
            
        if(yes('Do you want to find the maximum/minimum value of  family with four or more ownership rate ?')):
            kind='fourorMore'
            node_with_max = max(tree_nodes, key=lambda node: node.fourorMore)
            node_with_min = min(tree_nodes, key=lambda node: node.fourorMore)
            print("Minimum value:", node_with_min.fourorMore,'State:',node_with_min.state,'Year:',node_with_min.year)
            print("Maximum value:", node_with_max.fourorMore,'State:',node_with_max.state,'Year:',node_with_max.year)
            break
            
        if(yes('Do you want to find the maximum/minimum value of  BirthRate ?')):
            kind='BirthRate'
            node_with_max = max(tree_nodes, key=lambda node: node.BirthRate)
            node_with_min = min(tree_nodes, key=lambda node: node.BirthRate)
            print("Minimum value:", node_with_min.BirthRate,'State:',node_with_min.state,'Year:',node_with_min.year)
            print("Maximum value:", node_with_max.BirthRate,'State:',node_with_max.state,'Year:',node_with_max.year)
            break
            
        if(yes('Do you want to find the maximum/minimum value of  TotalPopulation ?')):
            kind='TotalPopulation'
            node_with_max = max(tree_nodes, key=lambda node: node.TotalPopulation)
            node_with_min = min(tree_nodes, key=lambda node: node.TotalPopulation)
            print("Minimum value:", node_with_min.TotalPopulation,'State:',node_with_min.state,'Year:',node_with_min.year)
            print("Maximum value:", node_with_max.TotalPopulation,'State:',node_with_max.state,'Year:',node_with_max.year)
            break
         
        if(yes('Do you want to find the maximum/minimum value of  total tourist attraction number ?')):
            kind='ta_number'
            node_with_max = max(tree_nodes, key=lambda node: node.ta_number)
            node_with_min = min(tree_nodes, key=lambda node: node.ta_number)
            print("Minimum value:", node_with_min.ta_number,'State:',node_with_min.state,'Year:',node_with_min.year)
            print("Maximum value:", node_with_max.ta_number,'State:',node_with_max.state,'Year:',node_with_max.year)
            break
            
        print('Please choose at least one attribute.')


  elif option == "3":
    while True:
        try:
            state = input("Enter the name of the state: ")
            if state in valid_state:
                break
            else:
                 print("Invalid state. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a  state.")
    print_tourist_attraction(state)
  elif option == "4":
    while True:
        try:
            year = int(input("Enter a year between 2009 and 2017: "))
            if 2009 <= year <= 2017:
            # Year is valid, so we can exit the loop
                break
            else:
                print("Invalid year. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a numeric year.")
    while True:
        if(yes('Do you  want to find the maximum/minimum value of family with zero cars ownership rate ?')):
            
            node_with_max = max(tree_node[year], key=lambda node: node.zero)
            node_with_min = min(tree_node[year], key=lambda node: node.zero)
            print("Minimum value:", node_with_min.zero,'State:',node_with_min.state,'Year:',node_with_min.year)
            print("Maximum value:", node_with_max.zero,'State:',node_with_max.state,'Year:',node_with_max.year)
            break

        if(yes('Do you want to find the maximum/minimum value of  family with one car ownership rate ?')):
            
            node_with_max = max(tree_node[year], key=lambda node: node.one)
            node_with_min = min(tree_node[year], key=lambda node: node.one)
            print("Minimum value:", node_with_min.one,'State:',node_with_min.state,'Year:',node_with_min.year)
            print("Maximum value:", node_with_max.one,'State:',node_with_max.state,'Year:',node_with_max.year)
            break
        if(yes('Do you want to print family with one or more cars ownership rate ?')):
            kind='oneorMore'
            node_with_max = max(tree_node[year], key=lambda node: node.oneorMore)
            node_with_min = min(tree_node[year], key=lambda node: node.oneorMore)
            print("Minimum value:", node_with_min.oneorMore,'State:',node_with_min.state,'Year:',node_with_min.year)
            print("Maximum value:", node_with_max.oneorMore,'State:',node_with_max.state,'Year:',node_with_max.year)
            break
            
        if(yes('Do you want to find the maximum/minimum value of  family with two or more cars ownership rate ?')):
            kind='twoorMore'
            node_with_max = max(tree_node[year], key=lambda node: node.twoorMore)
            node_with_min = min(tree_node[year], key=lambda node: node.twoorMore)
            print("Minimum value:", node_with_min.twoorMore,'State:',node_with_min.state,'Year:',node_with_min.year)
            print("Maximum value:", node_with_max.twoorMore,'State:',node_with_max.state,'Year:',node_with_max.year)
            break
            break
        if(yes('Do you want to find the maximum/minimum value of  family with three or more cars ownership rate ?')):
            kind='threeorMore'
            node_with_max = max(tree_node[year], key=lambda node: node.threeorMore)
            node_with_min = min(tree_node[year], key=lambda node: node.threeorMore)
            print("Minimum value:", node_with_min.threeorMore,'State:',node_with_min.state,'Year:',node_with_min.year)
            print("Maximum value:", node_with_max.threeorMore,'State:',node_with_max.state,'Year:',node_with_max.year)
            break
            
        if(yes('Do you want to find the maximum/minimum value of  family with four or more ownership rate ?')):
            kind='fourorMore'
            node_with_max = max(tree_node[year], key=lambda node: node.fourorMore)
            node_with_min = min(tree_node[year], key=lambda node: node.fourorMore)
            print("Minimum value:", node_with_min.fourorMore,'State:',node_with_min.state,'Year:',node_with_min.year)
            print("Maximum value:", node_with_max.fourorMore,'State:',node_with_max.state,'Year:',node_with_max.year)
            break
            
        if(yes('Do you want to find the maximum/minimum value of  BirthRate ?')):
            kind='BirthRate'
            node_with_max = max(tree_node[year], key=lambda node: node.BirthRate)
            node_with_min = min(tree_node[year], key=lambda node: node.BirthRate)
            print("Minimum value:", node_with_min.BirthRate,'State:',node_with_min.state,'Year:',node_with_min.year)
            print("Maximum value:", node_with_max.BirthRate,'State:',node_with_max.state,'Year:',node_with_max.year)
            break
            
        if(yes('Do you want to find the maximum/minimum value of  TotalPopulation ?')):
            kind='TotalPopulation'
            node_with_max = max(tree_node[year], key=lambda node: node.TotalPopulation)
            node_with_min = min(tree_node[year], key=lambda node: node.TotalPopulation)
            print("Minimum value:", node_with_min.TotalPopulation,'State:',node_with_min.state,'Year:',node_with_min.year)
            print("Maximum value:", node_with_max.TotalPopulation,'State:',node_with_max.state,'Year:',node_with_max.year)
            break
         
        if(yes('Do you want to find the maximum/minimum value of  total rourist attraction number ?')):
            kind='ta_number'
            node_with_max = max(tree_node[year], key=lambda node: node.ta_number)
            node_with_min = min(tree_node[year], key=lambda node: node.ta_number)
            print("Minimum value:", node_with_min.ta_number,'State:',node_with_min.state,'Year:',node_with_min.year)
            print("Maximum value:", node_with_max.ta_number,'State:',node_with_max.state,'Year:',node_with_max.year)
            break
            
        print('Please choose at least one attribute.')
  else:
    print("Invalid option")


# In[77]:


def main():

    print("Welcome!")
    playagain=True
    while playagain:
        user_options()
        playagain=yes("Do you want to play again?")
    print("Bye!")
if __name__ == '__main__':
    main()


# In[75]:


# user_options()


# In[ ]:





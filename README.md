# SI507 Final Project

Welcome to the Project!

This project aims to retrieve and analyze various data points for each state in the United States, including car ownership rate, birth rate, and tourist attractions.

## Prerequisites

Before you begin, make sure you have the following libraries installed:

- pandas
- BeautifulSoup (bs4)
- requests
- json
- os
- csv
- tqdm

To install these libraries, you can use `pip install `.

## Installation

To get started with the project, follow these steps:

1. Clone the repository to your local machine:

```shell
Copy codegit clone https://github.com/sjtuxueguanhua/SI507Final-Project.git
```

1. Navigate to the project directory:

```
Copy codecd SI507Final-Project
```

1. Run the script:

```
Copy codepython final_project.py
```

## Usage

This project is aimed at four main usages:

1. Display an specific data for a state of a certain year

2. Get maximum/min value of a kind of data of all periods

3. Display all the attractions of a state

4. Enter a year, return the maximum/min value of a state

The data kinds include:

`state`:name of the state

`year`: year of the data

`zero`:family with zero cars ownership rate

`one`:family with one car ownership rate

`oneorMore`:family with one or more cars ownership rate

`twoorMore`:family with two or more cars ownership rate

`threeorMore`:family with three or more cars ownership rate

`fourorMore`:family with four or more ownership rate

`BirthRate `:BirthRate of the state of the year

`TotalPopulation`:TotalPopulation of the state of the year

`tourist_attraction_list`:tourist attraction list of the state

`ta_number`: total tourist attraction number

## Data Structure

The data structure is a graph in the organization of Year as top tree and each state as subtree.

```shell
                               Year1
                              /    \
                             /      \
                            /        \
                           /          \
                          /            \
						State 1  ...   State N
  						 |               |
  					 zero...ta_number  zero...ta_number             


```



## Contributing

If you want to contribute to the project, follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b new-feature`.
3. Make your changes and commit them: `git commit -m "Add new feature"`.
4. Push the new branch to your fork: `git push origin new-feature`.
5. Create a new pull request.

## License

This project is licensed under the [MIT License](https://chat.openai.com/LICENSE).

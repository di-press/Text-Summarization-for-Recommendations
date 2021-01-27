# Text-Summarization-refactored

> - [Setup](#Setup)
> - [How to generate needed files/databases](#Files/db's)
> - [Passing parameters](#Parameters)
> - [How to adapt my dataset?](#Dataset)
> - [About](#About)


<!-- -->
## Setup
Files/directories and other dependencies needed:

    All directories above should be inside the directory of this project:

* single_reviews_corenlp (directory): can be generated in the next section if you are using the dataset (colocar o link do Dataset aqui)(Files/db's section). If you want to use other dataset, see section #Dataset;
* BNC_nouns.db: can be generated in the next section (Files/db's section);
* stanford-corenlp-4.2.0 (library): must be downloaded at https://stanfordnlp.github.io/CoreNLP/download.html (just click the red button "Download CoreNLP 4.2.0")

![printscreen of the files/directory inside the project folder](directory_demo.png?raw=True "How your directory should be:")

## Files/db's

To generate the files/directories needed in the section above, you need:

* ota_20.500.12024_2554 (BNC corpus - British National Corpus): must be downloaded
(Not finished yet)

## Parameters

Start by reading the "paper_pipeline.py". Its logic follows the sequence of steps described in the paper.
In the main function of "paper_pipeline.py", adjust the following parameters:

* KL_threshold (int): the threshold of KL selection described in the paper
* top_k_number(int): the number of "top_k" aspects ranked; as an example, if top_k_number = 5,
 the top-5 aspects of an item are selected
* generate_BNC_db: set to "True" if you never have generated "BNC_nouns.db" before
* generate_single_corenlp_reviews: set to "True" if you have never generated your dataset before.

## Dataset
If you don't want to use the dataset (colocar link dataset aqui), you can adapt your dataset
following these steps:
To do

## About
Detailed pipeline:
To do
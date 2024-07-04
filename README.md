# Read This Before Editing Data

#### The organization of this file is extremely important. You must understand, and abide by, the system.

I am going to go through each folder and its purpose.



1. processing

- This folder stores all Python files used for processing the data.
- processing.py contains functions to write out data into the necessary format for both intent and NER models
- data_helper_functions.py contains every other function we use to process data. For example, deleting duplicates, or removing any line with a specific phrase. If you ever need something like this done, please check for the necessary function within the file first. If it is not there, create your own function and provide an explaination of it for others to use.



2. Intent

- This folder contains all data relating exclusively to the Intent model(s). There are many groupings of data that can apply to both NER and Intent, such as dynamic prompted input sentences, things like this should not go in here.
- The folder contains many sub-folders, each relating to a meaningful grouping of intents, easily decipherable based on the names.
- Each of these sub-folders should contain finalized outputs and base datasets.
- There is also a Final-Datasets sub-folder. This should contain only the completely finalized dataset for the intent model(s)



3. NER

- This folder is very similar to the Intent folder. It contains multiple folders relating to meaningful groupings of NER data. Each Order and Reservation folder should contain finished data relating to the NER for these groupings.
- Filler-Data holds files with filler data for dynamic sentences, our processing files will automatically insert random lines from these files into empty labels in dynamic sentences.




6. Order-Specifics and Reservation-Specifics

- These two folders are very similar. They contain data that is specific to each pipeline and sectioned into meaningful groupings. It is very helpful to keep data separated into files such as prompted inputs and separate intents, then combine the data when you are compiling for a new model.



That's the end for now. If you have any questions please bring it up to me(Travis) as soon as possible and I can amend the document.

Again, **this is very important**. Unorganized data will lead to more sloppy models, wasted time, and wasted money. 

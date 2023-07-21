# DSCO

In this repository I will store the codes developed during my rotation at [Development of the spinal cord organization](https://www.ibps.sorbonne-universite.fr/en/research/neuroscience/development-of-the-spinal-cord-organization) team.

## Contents

- [Environment](#environment)
    - [Repository files](#repository-files)
    - [Installation](#installation)
- [C.I.T.R.O.N Jaune](#citron-jaune)  
    - [How to use it](#how-to-use-it)
    - [Folder organization](#folder-organization)
    - [results.xlsx](#resultsxlsx)
    - [Troubleshooting](#troubleshooting)
    - [Hints](#hints)
- [Contributing](#contributing)
- [References](#references)
- [Developers](#developed-by-agathe-lafont-lafont-and-tulio-almeida)   

## Environment

To use the codes it is necessary to install pyimagej (library to use ImageJ through python), for this it will be necessary to use:

If you prefer to use plain pip, or pip with virtualenv,
you will need to install the following things:
- Windows
    - The code has not been tested on linux and in this version is not working on macOS because of the interface (check [Troubleshooting](#troubleshooting)).
- [conda](https://conda.io), or you can use:
    - [miniconda](https://docs.conda.io/en/latest/miniconda.html)
    - [mamba](https://mamba.readthedocs.io/en/latest/)
- Python 3.8
- OpenJDK 8 or 11 – any flavor is fine [Zulu JDK+FX 8](https://www.azul.com/downloads/zulu-community/?version=java-8-lts&package=jdk-fx) works well
- [Apache Maven](https://maven.apache.org/)

### Repository files

    .
    ├── code                      # Folder with all the code
    │   ├── environment.yml       # File to create the conda env   
    │   ├── citron_jaune.ipynb    # Pipeline notebook
    │   ├── citron_jaune.py       # Pipeline script
    │   ├── citron.ico            # GUI icon
    │   └── functions.py          # Functions used in the pipeline
    ├── docs                      # Files to support the README file                                        
    └── README.md

### Installation

1. Install the OpenJDK updating the [path](https://www.java.com/en/download/help/path.html) 
    - How to [test it](https://www.baeldung.com/find-java-home)
2. Install maven updating the [path](https://www.java.com/en/download/help/path.html) 
    - How to [test it](https://stackoverflow.com/questions/24221361/checking-maven-version)
3. Install conda
4. Create the environment
    - clone this repository
    - using the terminal (_cd_ command [tutorial](https://fernando-mc.github.io/python3-workshop/navigating-with-a-terminal.html)) go to the repo code folder (or the folder that you put the environment.yml file)
    - type `conda env create`, or the mamba/miniconda command
5. After the instalation you can check it by activating the repo `conda activate citron` 

## C.I.T.R.O.N Jaune

This is the general pipeline to peform the analysis of the Calcium Image from spinal cords using the Regions of Interest (ROI) manager of ImageJ through Python.

<p align="center">
  <img width="500" height="400" src="https://github.com/tuliofalmeida/dsco/blob/main/docs/gp_gui.png">
</p>

### How to use it

1. Check the [installation guide](#installation)
2. Start the pipeline using the citron_jaune.ipynb using the VSCode and choose the **citron (Python 3.8.13)** enviroment as kernel, or use the .py script through the terminal using the command `conda run -n citron --live-stream python citron_jaune.py` in the folder that you saved the script (don't need to activate the env). P.S.: It's possible to use the Jupyter (type `jupyter notebook` after activate the env), but I didn't test the GUI using Jupyter directly. The .ipynb or the .py should be in the same folder as the functions.py file.
3. Determine the parameters in the GUI
    - Choose Folder: this button will open a window which you should pick the folder with the .cxd and .tif files for analysis ([folder organization](#folder-organization)).
    - ROIs: Choose the amount of ROI that you want in your analysis. The pipeline works using pairs of ROI's (2,4,6...), but the option of 3 ROIs will measure calcium dynamics of the activation and will save it as another .xlsx file.
    - Experiment: Experiment to be analyzed,, Electrostimulation ('Electro') or Optogenetical stimulation ('Opto') when using the entire spinal cord or pick Slice ('Slice') when the data are from spinal cord slices. Each type of experiment has a different image processing routine.
    - Obj size: The objective used during the data acquisition, this will change the pixel value to perform the conversion.
    - Lat. Dis.: Lateral Distance, if 'Yes' after you choose all the ROIs that you previously determined, will be possible to pick an extra one. This ROI is expected to be used to take the width (lateral distance) of the propagation.
    - RUN: this button will start the analysis
4. Pipeline Flow: The pipeline will run in all files available in the chosen folder using the parameters previously determined, it's import to organize the files with this information in mind. The first step will be create one .xlsx file using the amount of ROIs as reference. After this the pipeline will check if the file was already analyzed, if yes, this one will be skiped.
5. After choosing the parameters, will pop up one interactive plot with the frame that present the activation peak. In this plot you will determine the ROI's using the following commands:
    - Mouse Right Click: will draw  of the corner of the rectangle
    - Mouse Left Click: will draw the opposite corner of the rectangle
    - Space: Will confirm the ROI marking
    - b: will go back to the previus ROI in case of errors
    - P.S.: In case you want to skip the file, just create the ROIs in the upper left corner  (closer to the Y zero as possible), in this case the metrics will be skipped also and filled with zeros in the .csv file.
6. The pipeline will compute the metrics for this file and write it on the .xlsx file.
7. Outputs: In the chosen folder the .xlsx file will be saved using the name of the folder as reference (folder_results.xlsx). The pipeline will create one folder for each data containing:
    - Derivative substraction (file_subs.tif)
    - Data substraction minus the average (file_z_subs.tif)
    - Plot with every chosen ROI  (file_roi.svg)
    - Plot with ROIs peak and width (file_width_plot.svg)
    - ImageJ coords for all ROIs (file_roi.zip)
    - ImageJ multimeasure raw data (file.csv)
    - P.S.: in case you pick the 3 ROIs in the GUI, it will have specific plots, zip csv file for the 3 ROIs analysis (file_3_roi.svg,file_width_plot_3_ROI.svg,file_3_roi.zip,file_3_roi.csv).
8. It is necessary to restart the environment after each folder analysed.

### Folder organization

This is how your folder should be organized before the analysis

    .
    ├── ...
    ├── data_electro                      # Experiment folder with the data (folder to chose in the GUI)
    │   ├── 23.01.01.cxd                  # Raw data   
    │   ├── 23.01.02.cxd              
    │   ├── 23.01.03.cxd             
    │   ├── 23.01.04.cxd              
    │   ├── 23.01.05.cxd             
    │   └── 23.01.06.cxd                                                                                                            
    └── ...

After the analysis

    .
    ├── ...
    ├── data_electro                       # Experiment folder with the data
    │   ├── 23.01.01_analysis
    │        ├── 23.01.01.csv              # Multi-measure ROIs data
    │        ├── 23.01.01_roi.svg          # Plot in .svg to see the placed ROIs
    │        ├── 23.01.01_roi.zip          # ROIs coordinated done by ImageJ
    │        ├── 23.01.01_subs.tif         # Subtract the stacks
    │        ├── 23.01.01._width_plot.svg  # Plot with the peak and the other metrics
    │        └── 23.01.01_z_subs.tif       # Subtracted stacks minus the average  
    │   ├── 23.01.02_analysis           
    │   ├── 23.01.03_analysis              
    │   ├── 23.01.04_analysis             
    │   ├── 23.01.05_analysis              
    │   ├── 23.01.06_analysis             
    │   ├── 23.01.01.cxd 
    │   ├── 23.01.02.cxd           
    │   ├── 23.01.03.cxd              
    │   ├── 23.01.04.cxd             
    │   ├── 23.01.05.cxd              
    │   ├── 23.01.06.cxd  
    │   ├── data_electro_3ROI_results.xlsx # Results in the excel format for 3 ROIs analysis            
    │   └── data_electro_results.xlsx      # Results in the excel format                                                                
    └── ...

### results.xlsx

The .xlsx file header:
- File: file name
- Distance Midline: If '_Lat. Dis._' = Yes in the GUI will measure the width of the extra ROI, used to measure the from the midline to the lateral column, else will save 'NO EXTRA ROI'
- Frame used: The frame used to pick the ROIs (peak activation)
    For each ROI (metrics using scipy 'find_peaks() and peak_widths()'):
    - Half Rise ROI X: time taken for activation to reach half peak
    - Half Width ROI X: time taken between half peak and half decay
    - Rise ROI X: time taken for activation to reach peak (using 10/90)
    - Decay ROI X: time taken for activation from peak to baseline (using 10/90)
    For each pair (the first with the second and so on):
    - Distance ROI X-Y: distance between ROI's in $\mu m$
    - Speed ROI X-Y: speed for the activation to transit between the ROI's $\mu m/s$
- ps: For the slice pipeline the xlxs structure is the same

### Troubleshooting

1. Java errors when trying to run the pipeline 
    - This is proabaly related to the java installation, check the paths and will probably work
2. Java memory error (OOM)
    - The pipeline was developed using a windows computer with 32GB RAM and it worked without problems with almost 8GB available to Java Virtual Machine (using less then 4GB). In you have this problem, maybe this [link can help](https://forum.image.sc/t/out-of-memory-all-available-memory-247mb-has-been-used/10832/20). Long videos have a tendency to generate this problem, you may need to cut the videos.
3. I did the analysis and I didn't like ROIS placement
    - You can re-run only this data by deleting all the files in the corresponding folder, the pipeline will re-run only it and rewrite the xlsx only on this line.
4. xlsx Permisson denied
    - This error occurs when you run the pipeline with the .xlsx file open, it is necessary to close it for python to access and save the data.
5. Using in Linux (Ubuntu) or macOS
    - The only problem found with the other OS was the library used to create the interface (tkinter), probably the code will work removing the interface and passing the parameters manually or creating another interface (using PyQt). For this you will need a basic knowledge of python. The codes were written using procedural programming, for ease of editing and use.
6. Plot to pick ROIs in bad shape
    - The size of the plot was hardcoded to be full screen (=/), you can change it at line 555 (`fig,ax = plt.subplots()` and pass the parameter that you want `figsize=('x','y')` - x and y must be intergers according to your screen/resolution)
7. Log file
    - There is no log file from this pipeline, but, it's possible to check the errors and the progressing of the analysis (which file is under analysis and the steps) in the terminal.
8. The original ImageJ is not available in this environment
    - you just need to restart the environment, because isn't possible to re-import the ImageJ

### Hints

1. All files will be saved on the specific folder, you can check every step in ImageJ (opening the processed .tif files, the ROIs and re-do the metrics). Also, there is the .csv that you can use to do other analysis.
2. After starting the analysis of a folder do not add more data as it may overwrite some other data.
3. Dont change the number or ROIs between each file, or you will have some problems with the .xlsx header. In case that you need to have diferent ROIs it's better to group your files based on the amount of ROIs or start with the biggest one to create the .xlsx with the right header, but this can create errors.

## Contributing

For minor fixes of code and documentation, please go ahead and submit a pull request.  A gentle introduction to the process can be found [here](https://www.freecodecamp.org/news/a-simple-git-guide-and-cheat-sheet-for-open-source-contributors/).

Check out the list of issues that are easy to fix. Working on them is a great way to move the project forward.

Larger changes (rewriting parts of existing code from scratch, adding new functions to the core, adding new libraries) should generally be discussed by opening an issue first. PRs with such changes require testing and approval.

Feature branches with lots of small commits (especially titled "oops", "fix typo", "forgot to add file", etc.) should be squashed before opening a pull request. At the same time, please refrain from putting multiple unrelated changes into a single pull request.

## References

Feel free to use this code and edit it! If you use our code we kindly as that you please cite our repository!

## Developed by [Agathe Lafont](https://www.linkedin.com/in/agathe-g-lafont-453a80161/) and [Tulio Almeida](https://tuliofalmeida.com/)

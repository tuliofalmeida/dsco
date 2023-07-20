# DSCO

In this repository I will store the codes developed during my rotation at [DSCO](https://www.ibps.sorbonne-universite.fr/en/research/neuroscience/development-of-the-spinal-cord-organization).

## Environment

To use the codes it is necessary to install pyimagej (library to use ImageJ through python), for this it will be necessary to use:

If you prefer to use plain pip, or pip with virtualenv,
you will need to install the following things:
- Windows
    - The code has not been tested on linux and in this version is not working on macOS because of the interface, if you wanted to change the code by creating another interface or use without interface, it will work on linux and macOS probably.
- [conda](https://conda.io), or you can use:
    - [miniconda](https://docs.conda.io/en/latest/miniconda.html)
    - [mamba](https://mamba.readthedocs.io/en/latest/)
- Python 3.8
- OpenJDK 8 or 11 – any flavor is fine [Zulu JDK+FX 8](https://www.azul.com/downloads/zulu-community/?version=java-8-lts&package=jdk-fx) works well
- [Apache Maven](https://maven.apache.org/)

### Instalation

1. Install the OpenJDK updating the [path](https://www.java.com/en/download/help/path.html) 
    - How to [test it](https://www.baeldung.com/find-java-home)
2. Install maven updating the [path](https://www.java.com/en/download/help/path.html) 
    - How to [test it](https://stackoverflow.com/questions/24221361/checking-maven-version)
3. Install conda
4. Create the environment
    - clone this repository
    - using the terminal (_cd_ command [tutorial](https://fernando-mc.github.io/python3-workshop/navigating-with-a-terminal.html)) go to the repo main folder (or the folder that you put the citron.yml file)
    - type `conda env create`, or the mamba/miniconda command
5. After the instalation you can check it activatin the repo `conda activate citron` 

## C.I.T.R.O.N Jaune

This is the general pipeline to peform the analysis of the Calcium Image from spinal cords using the Regions of Interest (ROI) manager of ImageJ.

### How to use it

1. Check the installation guide
2. Start the pipeline using the .ipynb using the VSCode and choose the **citron (Python 3.8.13)** enviroment as kernel, or use the .py script through the terminal using the command `conda run -n citron --live-stream python citron.py` in the folder that you saved the script. ps: It's possible to use the Jupyter (type `jupyter notebook` after activate the env), but I didn't tested the GUI using Jupyter directly. The .ipynb or the .py should be in the same folder as the functions.py file.
3. Determine the parameters in the GUI
    - Choose Folder: this button will open a window which you should pick the folder with the .cxd and .tif files for analysis (Check Folder organization).
    - ROIs: Choose the amount of ROI that you want in your analysis. The pipeline works using pairs of ROI's (2,4,6...), but the option of 3 ROI's will run dynamics of the activation and will save it as another .xlsx file.
    - Stim: The type of the stimulation used, Electrostimulation ('Electro') or Optogenetical stimulation ('Opto'). Each type of stimulation has a different image processing.
    - Obj size: The objective used during the data acquisition, this will change the pixel value to perform the conversion.
    - Lat. Dis.: Lateral Distance, if 'Yes' after you choose all the ROI's that you previously determined, will be possible to pick an extra one. This ROI is expected to be used to take the width (lateral distance) of the propagation.
    - RUN: this button will start the analysis
4. Pipeline Flow: The pipeline will run in all files available in the choosed folder using the parameters previously determined, it's import to organize the files with this information in mind. The first step will be create one .xlsx file using the amount of ROI's as reference. After this the pipeline will check if the file was already analized, if yes, this one will be skiped.
5. After choosing the parameters, will pop up one interactive plot with the frame that present the activation peak. In this plot you will determine the ROI's using the following commands:
    - Mouse Right Click: will draw one of the diagonals of the rectangle
    - Mouse Left Click: will draw the other diagonal of the rectangle
    - Space: Will confirm the ROI marking
    - b: will go back to the previus ROI in case of errors
    - ps: In case you want to skip the file, just create the ROI's in the upper left corner  (closer to the Y zero as possible), in this case the metrics will be skipped also and filled with zeros in the .csv file.
6. The pipeline will compute the metrics for this file and write it on the .xlsx file.
7. Outputs: In the folder chosed the .xlsx file will be saved using the name of the folder as reference (folder_results.xlsx). The pipeline will create one folder for each data containing:
    - Data substraction (file_subs.tif)
    - Data substraction minus the average (file_z_subs.tif)
    - Plot with every ROI choosed (file_roi.svg)
    - Plot with ROIs peak and width (file_width_plot.svg)
    - ImageJ coords for all ROI's (file_roi.zip)
    - ImageJ multimeasure raw data (file.csv)
    - ps: in case you pick the 3 ROI in the GUI, will have specific plots, zip csv file for the 3 ROI's analysis (file_3_roi.svg,file_width_plot_3_ROI.svg,file_3_roi.zip,file_3_roi.csv).
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
    │        ├── 23.01.01.csv              # Multi-measure ROI's data
    │        ├── 23.01.01_roi.svg          # Plot in .svg to see the placed ROI's
    │        ├── 23.01.01_roi.zip          # ROI's coordinated done by ImageJ
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
    │   └── data_electro_results.xlsx      # Results in the excel format                                                                
    └── ...

### results.xlsx

The .xlsx file header:
- File: file name
- Distance Midline: If '_Lat. Dis._' = Yes in the GUI will measure the width of the extra ROI, used to measure the from the midline to the lateral column, else will save 'NO EXTRA ROI'
- Frame used: The frame used to pick the ROI's (peak activation)
    For each ROI (metrics using scipy 'find_peaks() and peak_widths()'):
    - Half Rise ROI X: time taken for activation to reach half peak
    - Half Width ROI X: time taken between half peak and half decay
    - Rise ROI X: time taken for activation to reach peak (using 10/90)
    - Decay ROI X: time taken for activation from peak to baseline (using 10/90)
    For each pair (the first with the second and so on):
    - Distance ROI X-Y: distance between ROI's in $m\mu$
    - Speed ROI X-Y: speed for the activation to transit between the ROI's $m\mu/s$

### Troubleshooting

1. Java errors when trying to run the pipeline 
    - This is proabaly related to the java instalation, check the paths and will probably work
2. Java memory error (OOM)
    - The pipeline was developed using a windows computer with 32GB RAM and it worked without problems with almost 8GB available to Java Virtual Machine (using less then 4GB). In you have this problem, maybe this [link can help](https://forum.image.sc/t/out-of-memory-all-available-memory-247mb-has-been-used/10832/20). Long videos have a tendency to generate this problem, you may need to cut the videos.
3. I did the analysis and I didn't like ROIS placement
    - You can re-run only this data by deleting all the files in the corresponding folder, the pipeline will re-run only it and rewrite the xlsx only on this line.
4. xlsx Permisson denied
    - This error occurs when you run the pipeline with the .xlsx file open, it is necessary to close it for python to access and save the data.
5. Using in Linux (Ubuntu) or macOS
    - The only problem found with the other OS was the library used to create the interface (tkinter), probably the code will work removing the interface and passing the parameters manually or creating another interface (using PyQt). For this you will need a basic knowledge of python. The codes were written using procedural programming, for ease of editing and use.
6. Plot to pick ROI's in bad shape
    - The size of the plot was hardcoded (=/), you can change it at line 442 (`fig,ax = plt.subplots(figsize = (20,15))`)

### Hints

1. All files will be saved on the specific folder, you can check every step in ImageJ (openning the processed .tif files, the ROI's and re-do the metrics). Also, there is the .csv that you can use to do other analysis.
2. After starting the analysis of a folder do not add more data as it may overwrite some other data.
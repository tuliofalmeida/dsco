# C.I.T.R.O.N Jaune

This is the general pipeline to peform the analysis of the Calcium Image from spinal cords using the Regions of Interest (ROI) manager of ImageJ.

## How to use it

1. Check the installation guide
2. Start the pipeline using the .ipynb using the VSCode and choose the **citron** enviroment as kernel. Or use the .py script through the terminal using the command `conda run -n citron --live-stream python general_pipeline.py` in the folder that you saved the script. If you did the instalation using mamba `mamba run -n citron --live-stream python general_pipeline.py`. **TEST IT**
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

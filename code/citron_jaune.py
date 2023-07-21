import os
import imagej
from tkinter import *
from tkinter import filedialog, simpledialog
from matplotlib.patches import Rectangle
from functions import *

ij = imagej.init('sc.fiji:fiji:2.5.0',mode='GUI')
ij.getVersion()

# Import jimport to use imagej plugins

from scyjava import jimport
Runtime = jimport('java.lang.Runtime')
print(Runtime.getRuntime().maxMemory() // (2**20), "MB available to Java")

# Import plugins

FolderOpener = jimport('ij.plugin.FolderOpener')
Duplicator = jimport('ij.plugin.Duplicator')
ImageCalculator = jimport('ij.plugin.ImageCalculator')
ZProjector = jimport("ij.plugin.ZProjector")()

# Interactive functions

def GUI():
    """
    This function have a class within to create a very
    simple interface that asks the user for the path of
    the file and the amount of ROIs to use. After this
    this function will create the file folder and the
    global path variables
    
    Parameters
    --------------
    None

    Returns
    --------------
    None

    Authors
    ------------
    Agathe Lafont and Tulio Almeida
    """    
    class PipelineGUI():
        def __init__(self, master):
            self.master=master
            self.master.title("C.I.T.R.O.N")
            self.master.geometry("500x400+10+10")
            self.master.attributes("-topmost", True)
            self.master.eval('tk::PlaceWindow . center')
            self.master['padx'] = 5
            self.master['pady'] = 5
            OPTIONS = [2,3,4,6,8,10,12,14,16]
            MODES = ['Electro','Opto','Slice']
            ZOOM = ['x4','x10']
            FIFTH = ['Yes','No']
            global folder_path
            
            # define GUI Widgets here
            
            # path button
            try:
                del folder_path
            except:
                pass
            self.pickFolderBtn = Button(master, text="Chose Folder", width=16,
                                        command = self.folderPicker,font=("Cordia New", 10))
            self.pickFolderBtn.place(x=180, y=70)
            
            # list of rois
            self.variable = StringVar(master)
            self.variable.set(OPTIONS[2]) # default value
            self.w = OptionMenu(master, self.variable, *OPTIONS)
            self.w.place(x=230, y=120)
            self.lbl_roi=Label(master, text="ROIs", fg='black', 
                               font=("Cordia New", 10))
            self.lbl_roi.place(x=190, y=125)

            # list of modes
            self.mode = StringVar(master)
            self.mode.set(MODES[0]) # default value
            self.w = OptionMenu(master, self.mode, *MODES)
            self.w.place(x=230, y=165)
            self.lbl_roi=Label(master, text="Experiment", fg='black', 
                               font=("Cordia New", 10))
            self.lbl_roi.place(x=140, y=172)

            # list of objective size
            self.zoom = StringVar(master)
            self.zoom.set(ZOOM[1]) # default value
            self.w = OptionMenu(master, self.zoom, *ZOOM)
            self.w.place(x=230, y=210)
            self.lbl_roi=Label(master, text="Obj size", fg='black', 
                               font=("Cordia New", 10))
            self.lbl_roi.place(x=165, y=215)

            # distance measure
            self.dis = StringVar(master)
            self.dis.set(FIFTH[0]) # default value
            self.w = OptionMenu(master, self.dis, *FIFTH)
            self.w.place(x=230, y=260)
            self.lbl_roi=Label(master, text="Lat. Dis.", fg='black', 
                               font=("Cordia New", 10))
            self.lbl_roi.place(x=165, y=265)

            # close button
            self.quitBtn = Button(master, text="RUN!", width=10,
                                 command = self.paths,font=("Cordia New", 10))
            self.quitBtn.place(x=207, y=320)

            # title label
            self.lbl=Label(master, text="C.I.T.R.O.N Jaune", fg='black', 
                        font=("Cordia New", 15))
            self.lbl.place(x=150, y=20)

            # alfa label
            self.Lower_left = Label(master,text ='Alpha Version - Developed by Agathe Lafont and Tulio Almeida',font=("Cordia New", 10))
            self.Lower_left.place(relx = 0.03,rely = 1.0,anchor ='sw')

        # Functions for GUI 
        def folderPicker(self):
            global folder_path
            self.pathToFolder = filedialog.askdirectory()
            folder_path = self.pathToFolder
            folder_path = os.path.normpath(folder_path)

        def paths(self):
            global file_name,analysis_folder,path_stacks,path_files,n_rois,files_list,pipeline,zoom,px_value,dis_l
            assert folder_path != '', "You must choose the file!"
            file_name,analysis_folder,path_stacks,path_files,files_list = {},{},{},{},[]
            # files_list = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith('.cxd')]
            for filename in os.listdir(folder_path):
                if filename.endswith('.cxd'):
                    if filename.startswith('.'):
                        pass
                    elif 'Spon' not in filename:
                        files_list.append(os.path.join(folder_path, filename))
                if filename.endswith('.tif'):
                    if filename.startswith('Spon'):
                        files_list.append(os.path.join(folder_path, filename))
                    elif filename.startswith('spon'):
                        files_list.append(os.path.join(folder_path, filename))
            for idx,file in enumerate(files_list):
                os.chdir(os.path.dirname(folder_path))
                file_name[idx] = file.split(os.sep)[-1][:-4]
                analysis_folder[idx] = file.split(os.sep)[-1][:-4]+"_analysis"
                path_stacks[idx] = os.path.join(os.path.dirname(file), analysis_folder[idx])
                path_files[idx] = os.path.join(path_stacks[idx],file_name[idx])
                n_rois = int(self.variable.get())
                pipeline = self.mode.get()
                zoom = self.zoom.get()
                dis_l = self.dis.get()

                # If there is no folder for this dataset create one
                if not os.path.exists(path_stacks[idx]):
                    print("Creating the {} folder".format(file_name[idx]))
                    os.makedirs(path_stacks[idx])
            
                path_stacks[idx] = path_stacks[idx] + os.sep
                
            self.master.destroy()
            self.master.quit()
                     
    # Define Main loop end extract input variables
    master = Tk()
    
    GUI=PipelineGUI(master)
    master.mainloop()
    
def onclick(event):
    """
    Function to control the plot using the mouse click.
    In this case lines will be plotted accordingly to
    left and right mouse click. After this the coordinates
    of the clicks is saved. This event is called insed 
    the plot code that isn't a function.
    
    Parameters
    --------------
    key : None or str
        the key(s) pressed

    Returns
    --------------
        None

    Authors
    ------------
    Agathe Lafont and Tulio Almeida

    Reference:

    ------------   
    https://matplotlib.org/stable/users/explain/event_handling.html
    """
    global x,y,pause
    
    plt.cla()
    plt.imshow(frame,cmap = plt.cm.plasma, vmax = px_max)
    plt.title('File: {} - Frame: {}'.format(file_name[idx],str(frame_idx)), fontsize = 15)
    plt.text(3, -8, 'ROI '+str(count+1), bbox=dict(fill=False, edgecolor='red', linewidth=2))
    plt.text(3, -23, 'Press B to REMOVE the ROI', bbox=dict(fill=False, edgecolor='red', linewidth=2))
    plt.text(3, -38, 'Press Space to CONFIRM the ROI', bbox=dict(fill=False, edgecolor='red', linewidth=2))
    try:
        for temp in range(count):
            c1 = ax.add_patch( Rectangle((coords_plot[temp][0], coords_plot[temp][1]),
                                    coords_plot[temp][2], coords_plot[temp][3], 
                                    facecolor= 'none', edgecolor = 'white',
                                    linewidth = 2))
            rx, ry = c1.get_xy()
            cx = rx + c1.get_width()/2.0
            cy = ry + c1.get_height()/2.0
            ax.annotate(str(temp+1), (cx, cy), color='white', 
            fontsize=13, ha='center', va='center', weight='bold')
    except:
        pass
    try:
        x
    except:
        x = [0,0]
    try: 
        y
    except:
        y = [0,0]
    
    if str(event.button) == "MouseButton.LEFT":
        x[0], y[0] = int(event.xdata), int(event.ydata)

    elif str(event.button) == "MouseButton.RIGHT":
        x[1], y[1] = int(event.xdata), int(event.ydata)

    for i,j in zip(x,y):
        plt.axvline(i, color = 'white')
        plt.axhline(j, color = 'white')
        plt.draw()

def onkey(event):
    """
    Function to control the plot using the keyboard.
    In this case the plot will be closed after pressing
    the spacebar. This event is called insed the plot 
    code that isn't a function.
    
    Parameters
    --------------
    key : None or str
        the key(s) pressed

    Returns
    --------------
        None

    Authors
    ------------
    Agathe Lafont and Tulio Almeida

    Reference:
    ------------   
    https://matplotlib.org/stable/users/explain/event_handling.html
    """
    global x,y,pause,xp,yp,wp,hp,count
    if event.key == ' ':
        if count < n_rois:
            xp,yp,wp,hp = rect_values((x[1], y[1]),(x[0], y[0]))
            coords_plot[count] = [xp,yp,wp,hp]
            coord_left[count] = (x[0], y[0])
            coord_right[count] = (x[1], y[1])
            ctemp = ax.add_patch( Rectangle((xp, yp),wp, hp))
            center[count] = ctemp.get_center()
            count +=1
        else:
            xp,yp,wp,hp = rect_values((x[1], y[1]),(x[0], y[0]))
            coords_plot_w[count] = [xp,yp,wp,hp]
            count +=1
        fig.canvas.mpl_disconnect(cid)
        pause = False
    elif event.key == 'b':
        if count > 0:
            count -= 1
        else:
            count = 0

def img_electrical_stimulation(data):
    """
    ImageJ processing steps for
    electrical stimulation data.
    
    Parameters
    --------------
    data: ij.ImagePlus
        raw data
        
    Returns
    --------------
    z_subs : ij.ImagePlus
        processed data using Imagej

    Authors
    ------------
    Agathe Lafont and Tulio Almeida        
    """
    global path_z,path_sub_z,zoom
    
    # Create one copy of the data removing the first frame
    data_remove_first = data.crop("2-{}".format(data.shape[2]))

    # Create one copy of the data removing the last frame
    data_remove_last = data.crop("1-{}".format(data.shape[2]-1))

    # Check the dimensions
    print("Data shape:",str(data.getDimensions()),
        "\nRemove first:",str(data_remove_first.getDimensions()),
        "\nRemove last:",str(data_remove_last.getDimensions()))

    # Use image calculator to substract the two stacks
    subs = ImageCalculator.run(data_remove_first, data_remove_last, "Subtract create stack")
    print("Substraction shape:",str(subs.getDimensions()))

    # apply the 'Lookup Table' in subs
    ij.IJ.run(subs, "Fire", "")

    # Create the Z projector, using average and 30 frames
    z_project = ZProjector.run(data, "avg", 0, 30) 

    # Use image calcultator to remove the average from the data
    z_subs = ImageCalculator.run(data, z_project, "Subtract create stack")

    # apply the 'Lookup Table' in z_subs
    ij.IJ.run(z_subs, "Fire", "")

    # Check the dimensions
    print("Z Projection:",str(z_project.getDimensions()),
        "\nZ substraction:",str(z_subs.getDimensions()))
    
    #Rotate the images in large field
    if zoom == 'x4':
        ij.IJ.run(z_subs, "Rotate...", "angle=-35. grid=0 interpolation=None stack")
    else:
        pass

    # save the data
    path_z =  os.path.join(path_stacks[idx], file_name[idx] + "_subs")
    path_sub_z = os.path.join(path_stacks[idx], file_name[idx] + "_z_subs")
    ij.IJ.saveAs(subs, "Tiff", path_z )
    ij.IJ.saveAs(z_subs, "Tiff", path_sub_z)

    return z_subs

def img_optical_stimulation(data, plus):
    """
    ImageJ processing steps for
    optical stimulation data.
    
    Parameters
    --------------
    data: ij.ImagePlus
        raw data
    plus: int
        value to add to first frame with late
        
    Returns
    --------------
    z_subs : ij.ImagePlus
        processed data using Imagej

    Authors
    ------------
    Agathe Lafont and Tulio Almeida        
    """
    global path_z,path_sub_z
    # Rotate the raw data
    if plus == 1:
        ij.IJ.run(data, "Rotate 90 Degrees Left", "")

    # Image processing

    # Create one copy of the data removing the first frame
    data_remove_first = data.crop("2-{}".format(data.shape[2]))

    # Create one copy of the data removing the last frame
    data_remove_last = data.crop("1-{}".format(data.shape[2]-1))

    # Use image calculator to substract the two stacks
    subs = ImageCalculator.run(data_remove_first, data_remove_last, "Subtract create stack")
    print("Substraction shape:",str(subs.getDimensions()))

    # data in python format to get the right pixel to substract
    datapy = ij.py.from_java(data)

    max_v = [np.max(datapy.values[frame,:,:]) for frame in range(datapy.values.shape[0])]
    peaks_v, _ = find_peaks(max_v, prominence=max(max_v)//5, width=3)
    px_subs = peak_widths(max_v, peaks_v, rel_height=.95)

    if len(px_subs[0]) == 0:
        max_v = [np.max(datapy.values[frame,200:300,200:300]) for frame in range(datapy.values.shape[0])]
        peaks_v, _ = find_peaks(max_v, prominence=max(max_v)//5, width=3)
        px_subs = peak_widths(max_v, peaks_v, rel_height=.95)


    # Create the Z projector, using the first two frames of the optogenetical stimulation
    z_project = ZProjector.run(data, "max", int(px_subs[2])+plus, int(px_subs[2])+plus+1) 

    # Use image calculator to substract the two stacks
    z_subs = ImageCalculator.run(data, z_project, "Subtract create stack")
    print("Substraction shape:",str(z_subs.getDimensions()))

    # apply the 'Lookup Table' in subs
    ij.IJ.run(z_subs, "Fire", "")

    # Check the dimensions
    print("Z Projection:",str(z_project.getDimensions()),
        "\nZ substraction:",str(z_subs.getDimensions()))

    # save the data
    path_z =  os.path.join(path_stacks[idx], file_name[idx] + "_subs")
    path_sub_z = os.path.join(path_stacks[idx], file_name[idx] + "_z_subs")

    ij.IJ.saveAs(z_subs, "Tiff", path_sub_z)
    ij.IJ.saveAs(subs, "Tiff", path_z )

    return z_subs

def img_slice(data):
    """
    ImageJ processing steps for
    slice data.
    
    Parameters
    --------------
    data: ij.ImagePlus
        raw slice data
        
    Returns
    --------------
    z_subs : ij.ImagePlus
        processed data using Imagej

    Authors
    ------------
    Agathe Lafont and Tulio Almeida        
    """
    global path_z,path_sub_z,zoom
    
    # Create one copy of the data removing the first frame
    data_remove_first = data.crop("2-{}".format(data.shape[2]))

    # Create one copy of the data removing the last frame
    data_remove_last = data.crop("1-{}".format(data.shape[2]-1))

    # Check the dimensions
    print("Data shape:",str(data.getDimensions()),
        "\nRemove first:",str(data_remove_first.getDimensions()),
        "\nRemove last:",str(data_remove_last.getDimensions()))

    # Use image calculator to substract the two stacks
    subs = ImageCalculator.run(data_remove_first, data_remove_last, "Subtract create stack")
    print("Substraction shape:",str(subs.getDimensions()))

    # apply the 'Lookup Table' in subs
    ij.IJ.run(subs, "Fire", "")

    # Create the Z projector, using average and 30 frames
    z_project = ZProjector.run(data, "avg", 80, 90) 

    # Use image calcultator to remove the average from the data
    z_subs = ImageCalculator.run(data, z_project, "Subtract create stack")

    # apply the 'Lookup Table' in z_subs
    ij.IJ.run(z_subs, "Fire", "")

    # Check the dimensions
    print("Z Projection:",str(z_project.getDimensions()),
        "\nZ substraction:",str(z_subs.getDimensions()))    

    # save the data
    path_z =  os.path.join(path_stacks[idx], file_name[idx] + "_subs")
    path_sub_z = os.path.join(path_stacks[idx], file_name[idx] + "_z_subs")
    ij.IJ.saveAs(subs, "Tiff", path_z )
    ij.IJ.saveAs(z_subs, "Tiff", path_sub_z)

    return z_subs

# call the GUI
GUI()
print('Folder path:',folder_path)
print('Files:','\n'.join(files_list))
print('Number of ROIs:',n_rois)

# create the xlsx file for all experiments
xlsx_file = create_xlsx(folder_path,n_rois)

for idx,file in enumerate(files_list):
    
    if not os.listdir(path_stacks[idx]) and n_rois != 3:
        # Load the video
        data = ij.IJ.openImage(file)
        print('\n{} under analysis'.format(file.split(os.sep)[-1]))

        # define the pixel size based on zoom
        if zoom == 'x4':
            px_value = 6.5
        elif zoom == 'x10':
            px_value = 2.6

        # Measure of the fifth ROI
        if dis_l == 'Yes':
            dis_f = 1
        else:
            dis_f = 0
            
        # Image processing
        if pipeline == 'Electro':
            z_subs = img_electrical_stimulation(data)
            z_array = ij.py.from_java(z_subs)
        elif pipeline == 'Opto':
            plus = 1
            while True:
                z_subs = img_optical_stimulation(data, plus)
                z_array = ij.py.from_java(z_subs)
                if np.mean(z_array[0,:,:].values) < 2:
                    break
                else:
                    plus +=1
        elif pipeline == 'Slice':
            z_subs = img_slice(data)
            z_array = ij.py.from_java(z_subs)
       

        # delete the loaded raw imagej
        del data

        # ROI analysis 

        # Finding the highest pixel and the event frame
        px_min, px_max, frame_idx = frame_plot(z_array)
        print('Min px value:',px_min,'\nMax px value:',int(px_max),'\n')

        # Creating the rectangles areas in the event
        coord_right, coord_left = {},{}
        coords_plot,coords_plot_w = {},{}
        center = {}
        count = 0
        while count < n_rois +dis_f:
            try:
                del x,y,pause
            except:
                pass

            pause = True
            fig,ax = plt.subplots()
            frame = z_array[frame_idx]
            plt.imshow(frame,cmap = plt.cm.plasma, vmax = px_max)
            plt.text(3, -23, 'Press B to REMOVE the ROI', bbox=dict(fill=False, edgecolor='red', linewidth=2))
            plt.text(3, -38, 'Press Space to CONFIRM the ROI', bbox=dict(fill=False, edgecolor='red', linewidth=2))
            plt.text(3, -8, 'ROI '+str(count+1), bbox=dict(fill=False, edgecolor='red', linewidth=2))
            plt.title('File: {} - Frame: {}'.format(file_name[idx],str(frame_idx)), fontsize = 15)
            try:
                for temp in range(count):
                    c1 = ax.add_patch( Rectangle((coords_plot[temp][0], coords_plot[temp][1]),
                                            coords_plot[temp][2], coords_plot[temp][3], 
                                            facecolor= 'none', edgecolor = 'white',
                                            linewidth = 2))
                    rx, ry = c1.get_xy()
                    cx = rx + c1.get_width()/2.0
                    cy = ry + c1.get_height()/2.0
                    ax.annotate(str(temp+1), (cx, cy), color='white', 
                    fontsize=13, ha='center', va='center', weight='bold')
            except:
                pass
            plt.title('File: {} - Frame: {}'.format(file_name[idx],str(frame_idx)), fontsize = 15)
            cid = fig.canvas.mpl_connect('button_press_event', onclick)
            cid2 = fig.canvas.mpl_connect('key_press_event', onkey)
            fig.canvas.manager.full_screen_toggle()
            
            while pause:
                plt.pause(0.1)
            plt.close('all')

        # create the ROI areas in the imageJ format
        roi_areas = determined_rois(coord_left,coord_right,n_rois)

        # plot and save the ROIs determined by the user
        plot_rois(roi_areas, frame, px_max, file_name[idx], path_files[idx])

        # create the arguments for the macro
        args = {'inputFile': path_sub_z,
                'outputFile': path_files[idx],
                'windowImg': path_sub_z.split(os.sep)[-1],
                'roiFile': path_files[idx]}

        # create the macro 
        macro = roi_macro(roi_areas)

        # run the macro
        result = ij.py.run_macro(macro, args)


        # Propagation

        # load the csv data with the ImageJ analysis
        df = load_data(path_files[idx]+'.csv',n_rois=n_rois)

        if np.mean([value[0] for value in coord_left.values()]) > 10:
            # plot and save the curve for each ROI with peak and half peak
            fig,ax = plt.subplots()
            plot_peaks(df, n_rois,plot_title = '{} peaks'.format(file_name[idx]),ax = ax);
            plt.tight_layout()
            fig.savefig(path_files[idx]+'_width_plot.svg')
            plt.close()

            # get the half peak
            metrics,origin = half_peak(df, n_rois)
        else:
            metrics = {roi:[0,0,0,0] for roi in range(n_rois+1)}
            origin = 0
        
        # Distance analysis

        if np.mean([value[0] for value in coord_left.values()]) > 10:
            dis_metrics = measuraments(df,center,px_value)
        else:
            dis_metrics = {str(roi+1)+'-'+str(roi+2):[0,0] for roi in range(0,n_rois,2)}

        # xlsx file
        save_xlsx(xlsx_file,idx,metrics,dis_metrics,file_name,frame_idx,n_rois,coords_plot_w,px_value)

    #---------------------------------------------------------------------------------------------------    
    elif n_rois == 3:
        # Create the xlsx file
        xlsx_file = create_xlsx_3ROI(folder_path)

        # load the z_sub file and transform it to python
        data_z = file[:-4] + '_analysis' +os.sep +file_name[idx] +'_z_subs.tif'
        path_sub_z = file[:-4] + '_analysis' +os.sep +file_name[idx] +'_z_subs'

        # Loading and transforming and java image into a python image
        z_array = ij.IJ.openImage(data_z)
        z_array = ij.py.from_java(z_array)

        # Finding the highest pixel and the event frame
        px_min, px_max, frame_idx = frame_plot(z_array)
        print('Min px value:',px_min,'\nMax px value:',int(px_max),'\n')

        # Creating the rectangles areas in the event
        coord_right, coord_left = {},{}
        coords_plot,coords_plot_w = {},{}
        center = {}
        count = 0
        while count < n_rois:
            try:
                del x,y,pause
            except:
                pass

            pause = True
            fig,ax = plt.subplots(figsize = (20,15))
            frame = z_array[frame_idx]
            plt.imshow(frame,cmap = plt.cm.plasma, vmax = px_max)
            plt.text(3, -23, 'Press B to REMOVE the ROI', bbox=dict(fill=False, edgecolor='red', linewidth=2))
            plt.text(3, -38, 'Press Space to CONFIRM the ROI', bbox=dict(fill=False, edgecolor='red', linewidth=2))
            plt.text(485, -7, 'ROI '+str(count+1), bbox=dict(fill=False, edgecolor='red', linewidth=2))
            plt.title('File: {} - Frame: {}'.format(file_name[idx],str(frame_idx)), fontsize = 15)
            try:
                for temp in range(count):
                    c1 = ax.add_patch( Rectangle((coords_plot[temp][0], coords_plot[temp][1]),
                                            coords_plot[temp][2], coords_plot[temp][3], 
                                            facecolor= 'none', edgecolor = 'white',
                                            linewidth = 2))
                    rx, ry = c1.get_xy()
                    cx = rx + c1.get_width()/2.0
                    cy = ry + c1.get_height()/2.0
                    ax.annotate(str(temp+1), (cx, cy), color='white', 
                    fontsize=13, ha='center', va='center', weight='bold')
            except:
                pass
            plt.title('File: {} - Frame: {}'.format(file_name[idx],str(frame_idx)), fontsize = 15)
            cid = fig.canvas.mpl_connect('button_press_event', onclick)
            cid2 = fig.canvas.mpl_connect('key_press_event', onkey)
            
            while pause:
                plt.pause(0.1)
            plt.close('all')

        # create the ROI areas in the imageJ format
        roi_areas = determined_rois(coord_left,coord_right,n_rois)

        # plot and save the ROIs determined by the user
        plot_rois(roi_areas, frame, px_max, file_name[idx], path_files[idx]+'_3')

        # create the arguments for the macro
        args = {'inputFile': path_sub_z,
                'outputFile': path_files[idx]+'_3_roi',
                'windowImg': path_sub_z.split(os.sep)[-1],
                'roiFile': path_files[idx]+'_3'}

        # create the macro 
        macro = roi_macro(roi_areas)

        # run the macro
        result = ij.py.run_macro(macro, args)


        # Propagation

        # load the csv data with the ImageJ analysis
        df = load_data(path_files[idx]+'_3_roi.csv',n_rois=n_rois)

        if np.mean([value[0] for value in coord_left.values()]) > 10:
            # plot and save the curve for each ROI with peak and half peak
            fig,ax = plt.subplots()
            plot_peaks(df, n_rois,plot_title = '{} peaks'.format(file_name[idx]),ax = ax);
            plt.tight_layout()
            fig.savefig(path_files[idx]+'_3_roi_width_plot.svg')
            plt.close()

            # get the half peak
            metrics,origin = half_peak(df, n_rois)
        else:
            metrics = {roi:[0,0,0,0] for roi in range(n_rois+1)}
            origin = 0

        # xlsx file
        save_xlsx_3ROI(xlsx_file,idx,metrics,file_name,frame_idx)
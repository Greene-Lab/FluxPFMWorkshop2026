# Reliability Analysis Functions
import argparse,glob,json,logging,math,os,random,sys,time,warnings
import nibabel as nib
import numpy as np
import pandas as pd
import scipy.io

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.cm import Set2, tab20
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.patheffects as PathEffects
## suppress matplotlib warnings
mpl_logger = logging.getLogger('matplotlib')
mpl_logger.setLevel(logging.WARNING)

from itertools import cycle
from datetime import datetime


def create_raw_data(subid, data_dir, task, fd_thresh, TR, num_of_sessions):
        print(f'\n----Creating all visit, concatenated RAW data for {subid}----')
        # iterate and get all visits ptseries paths
        all_summaries = sorted(glob.glob(os.path.join(data_dir, 'derivatives', f'sub-{subid}','*')))

        # grab each ptseries, motion censor, and keep data for concatenation
        all_visit_data = []
        if num_of_sessions == "all":
            visits_to_process = all_summaries
        else:
            num_of_sessions = int(num_of_sessions)

            if num_of_sessions > len(all_summaries):
                sys.exit(f"You have exceeded the number of sessions collected for this participant. "
            f"Requested {num_of_sessions} sessions, but only {len(all_summaries)} sessions are available."
        )
            visits_to_process = all_summaries[:num_of_sessions]
        
        print(f"Processing {len(visits_to_process)} sessions:")
        
        for visit in visits_to_process:
            ptseries = glob.glob(os.path.join(visit,'Smoothed',f'*task-{task}_DCANBOLDProc_v4.0.0_Gordon_6.0mm_SMOOTHED.ptseries.nii'))
            if len(ptseries) == 1:
                pass
            else:
                sys.exit(f'Found multiple or NO 6mm smoothed ptseries (hardcoded for now to 6mm). Check summary dir! {ptseries} {visit}')
            ptseries_path = ptseries[0]
            print(os.path.basename(ptseries_path))
            ptseries_img = nib.load(ptseries_path)
            ptseries_data = ptseries_img.get_fdata()
            ptseries_data = np.transpose(ptseries_data, (1, 0))
            ptseries_data = np.array(ptseries_data)
            print("Shape of ptseries data array (parcels, frames collected):", ptseries_data.shape)

            fd_mat_path = glob.glob(os.path.join(visit, 'Motion', f'*task-{task}_motion_numbers.mat'))[0]
            print("Reading motion file:", os.path.basename(fd_mat_path))
            fd_mat = scipy.io.loadmat(fd_mat_path)

            # Get the framewise FD values
            fd_values = fd_mat['motion_numbers']['FD'][0, 0]

            # Create censor vector:
            # 0 = keep frame
            # 1 = reject frame
            del_vector = np.asarray(fd_values > fd_thresh).flatten()

            # Find indices of frames to reject
            delete_indices = list(np.where(del_vector == 1)[0])

            # Remove censored frames from ptseries data
            motion_censored_data = np.delete(ptseries_data, delete_indices, axis=1)
            print(f'   -Original frames: {ptseries_data.shape[1]}')
            print(f'   -Frames after censoring: {motion_censored_data.shape[1]}')
            print(f'      ')
            print(f'      ')
            if motion_censored_data.shape[1] < (300/TR):
                print('WARNING: Less than 5 min left after censoring at this FD!!!')
            else:
                pass
            all_visit_data.append(motion_censored_data)
        print(f'Total visits for sub-{subid}: {len(all_visit_data)}')
        # # shape check for neuroticism - can delete. Shape is used for the censored frames print above
        # for x in all_visit_data:
        #     print(x.shape)

        # concatenate all data
        raw_concatenated_data = np.concatenate(all_visit_data, axis=-1)
        print(f'Concatenated/Censored data shape (parcels, frames): {raw_concatenated_data.shape}')

        # print total available time
        seconds = math.floor(raw_concatenated_data.shape[1] * TR)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        print('Censored data in time: {:02d}Hours {:02d}Min {:02d}Sec'.format(hours, minutes, seconds))

        # clean up memory
        #print('...Memory cleanup')
        del(ptseries_img)
        del(ptseries_data)
        del(fd_mat)
        del(motion_censored_data)
        ## Quick check of how much memory being used
        sizes = {k: sys.getsizeof(v) for k,v in locals().items()}
        total_size_gb = sum(sizes.values()) / (1024**3)
        #print("Total memory used by variables: {:.2f} GB".format(total_size_gb))

        return raw_concatenated_data

def create_true(raw_concatenated_data, truetime, TR):
        # logger.debug(f'\n----Creating randomized TRUE data for {subid}---- DELETE ME LATER!!!!!')
        # make copy of raw concat data so that editing from pulling true data doesn't follow to subsequent loops
        concatenated_data = raw_concatenated_data.copy()
        if raw_concatenated_data.shape == concatenated_data.shape:
            pass
        else:
            sys.exit('Raw data shape is altered!!!! This is not right!')
        ## Create TRUE data from taking 5 minute samples, equally distributed across the total raw/censored data
        # Set the chunk size in minutes
        chunk_minutes = 5
        chunks_in_true = int(truetime / chunk_minutes)
        tr_5min = math.ceil(300 / TR)
        # Grab 5-minute chunks evenly distributed across the data to hour array
        available_cols = concatenated_data.shape[1]
        max_start_index = available_cols - (tr_5min + 1)
        #print(max_start_index)
        #the line below is updated to make this work for one visit for the PFM workshop. The normal line is: start_indices = np.random.choice(max_start_index, size=1000, replace=False)
        start_indices = np.random.choice(max_start_index, size=600, replace=False)
        #start_indices = np.random.choice(max_start_index, size=600, replace=False)
        #print(start_indices)
        check = 0
        for start_idx in start_indices:
            end_idx = start_idx + tr_5min
            chosen_chunk = concatenated_data[:,start_idx:end_idx].copy()    
            if np.count_nonzero(chosen_chunk == 999) > 0:
                pass
            else:
                concatenated_data[:, start_idx:end_idx] = 999
                if check > 0:
                    hour_array = np.concatenate((hour_array, chosen_chunk), axis=1)
                else:
                    hour_array = chosen_chunk.copy()
                    check = check + 1
                # stop at an hour of data, based on the TR)
                if hour_array.shape[1] == (chunks_in_true * tr_5min):
                    break
        # last remove all the used data to create remaining data array
        mask = np.all(concatenated_data == 999, axis=0)
        remaining_data = concatenated_data[:, ~mask]
        if (hour_array.shape[1] + remaining_data.shape[1]) == concatenated_data.shape[1]:
            pass
        else:
            sys.exit('lengths of arrays are bad. This should not happen anymore. Leaving check')

        # create true data corr mat
        true_data_mat = np.corrcoef(hour_array)
        # replace diag 1 with 0 for z transform (just to remove inf with 0)
        np.fill_diagonal(true_data_mat,0)
        # z transformed connectivity mat
        true_data_zmat = np.arctanh(true_data_mat)
        # put 1's back on the diag
        np.fill_diagonal(true_data_zmat,1)
        # logger.debug(f'True data shape: {true_data_zmat.shape}')

        ## quick check remaining time
        seconds = math.floor(remaining_data.shape[1] * TR)
        rem_hours = seconds // 3600
        rem_minutes = (seconds % 3600) // 60
        rem_seconds = seconds % 60
        # calc max minutes for ease in  workshop - can be defined otherwise if section below is uncommented
        max_minutes = ((seconds  // 60) // 5) * 5
        #print(f'Max minutes: {max_minutes}')
        #print('Remaining available data: {:02d}Hours {:02d}Min {:02d}Sec'.format(rem_hours, rem_minutes, rem_seconds))

        return hour_array, remaining_data, true_data_zmat, max_minutes

def plot_corrs(true_data,subid):
        logger.debug('\nCreating 15 min plots for TRUE data (ONLY first loop)')
        # print(true_data.shape)
        parts = np.split(true_data, 4, axis=1)
        for idx,p in enumerate(parts):
            if idx == 0:
                true_data_part = p
                min_marker = str((idx+1) * 15)
            else:
                true_data_part = np.concatenate((true_data_part, p), axis=1)
                min_marker = str((idx+1) * 15)
            # print(true_data_part.shape)
            # MAKE REORDERED TIMESERIES (for aesthetics)#
            reorder_indices = [9,63,64,65,66,67,68,69,76,101,103,159,170,223,226,229,
                            231,232,238,243,267,268,328,329,20,21,26,27,33,39,62,
                            70,71,75,80,81,83,100,102,104,110,111,146,152,179,180,
                            184,186,187,191,195,197,218,222,233,234,237,244,245,
                            247,248,273,316,317,11,88,92,172,253,0,3,5,24,25,43,93,
                            113,115,116,125,126,144,145,149,150,151,153,155,156,161,
                            164,183,185,199,219,224,256,258,277,278,289,314,315,320,
                            321,322,323,324,325,330,40,41,42,48,50,51,54,73,86,87,90,
                            91,94,99,105,106,109,112,154,188,198,202,207,210,235,249,
                            251,252,261,265,270,274,6,8,23,77,95,107,108,147,148,166,
                            167,169,181,239,259,260,271,272,275,276,318,319,326,327,
                            10,17,18,72,114,117,118,119,120,121,122,123,124,127,128,
                            132,133,134,141,143,158,171,177,178,279,280,281,282,283,
                            284,285,286,287,288,290,291,295,296,299,300,301,302,303,
                            304,305,311,313,12,13,129,142,173,293,294,312,28,82,182,
                            246,1,29,30,31,32,34,35,36,37,44,45,46,47,49,53,55,56,57,
                            162,189,190,192,193,194,200,201,203,204,205,206,208,209,
                            212,213,214,215,216,269,2,38,52,58,163,196,211,217,22,59,
                            60,61,74,78,79,84,85,157,160,220,221,225,227,228,230,236,
                            240,241,242,331,332,4,7,14,15,16,19,89,96,97,98,130,131,
                            135,136,137,138,139,140,165,168,174,175,176,250,254,255,
                            257,262,263,264,266,292,297,298,306,307,308,309,310]

            new_ts = true_data_part[reorder_indices]
            ## Get all the visuals info for this parcellation# 
            label_names = ['Auditory','CinguloOperc','CinguloParietal','Default','DorsalAttn','FrontoParietal','None',
                        'RetrosplenialTemporal','Salience','SMhand','SMmouth','VentralAttn','Visual']
            names_abbrev = ['Auditory','CingOperc','CingPar','Default','DorsalAtt','FrontoPar','None',
                            'RetroTemp','Salience','SMhand','SMmouth','VentralAtt','Visual']
            ## COLORS AND THINGS FOR CORR MATRIX IMAGE ##
            color_label_list = ['pink','purple','mediumorchid','red','lime','yellow','white',
                                'bisque','black','cyan','orange','teal','blue']
            # Range for color bars
            range_list = ['0-24','24-64','64-69','69-110','110-142','142-166','166-213',
                        '213-221','221-225','225-263','263-271','271-294','294-333']
            # CREATING numpy array of ranges #
            formatted_range_list = []                
            for rl in range_list:
                rl = rl.split('-')
                rl =  map(int, rl)
                formatted_range_list.append(list(rl))
            labels = np.array(formatted_range_list)
            # Index list for lines
            line_list = [24,64,69,110,142,166,213,221,225,263,271,294]
            # CREATE CORR MAT #
            piece_corr_mat = np.corrcoef(new_ts)
            # replace diag 1 with 0 for z transform (just to remove inf with 0)
            np.fill_diagonal(piece_corr_mat,0)
            # z transformed connectivity mat
            z_trans_mat = np.arctanh(piece_corr_mat)
            # put 1's back on the diag
            np.fill_diagonal(z_trans_mat,1)
            ## COLOR LABELED Z-TRANSFORMED MATRIX!
            fig, ax = plt.subplots()
            cmap = cm.get_cmap('jet')
            low_thresh = -0.4
            high_thresh = 1.0
            im = ax.imshow(z_trans_mat, aspect='equal',cmap=cmap,vmin=low_thresh,vmax=high_thresh)
            # DRAWING LINES #
            for the_line in line_list:
                ax.axhline(y=the_line - .5, linewidth=.5, color='white')
                ax.axvline(x=the_line - .5, linewidth=.5, color='white')
            # TITLE AND COLORBAR ADJUSTMENTS #
            ax.set_title(f'{subid} - {min_marker}min True Data Connectivity Matrix', fontsize=10)
            cbar = fig.colorbar(im, pad=0.0009)
            cbar.set_ticks([.8,.6,.4,.2,0,-0.2,-0.4,-0.6,-0.8])
            cbar.ax.set_ylabel('arctanh (z-transformed) values',rotation=270, labelpad=12, weight='bold')
            cbar.ax.tick_params(labelsize=5, pad=3)
            cbar.update_ticks()
            cbar.ax.yaxis.set_ticks_position('left')
            # CREATE AXES NEXT TO PLOT
            divider = make_axes_locatable(ax)
            axb = divider.append_axes("bottom", "10%", pad=0.02, sharex=ax)
            axl = divider.append_axes("left", "10%", pad=0.02, sharey=ax)
            axb.invert_yaxis()
            axl.invert_xaxis()
            axb.axis("off")
            axl.axis("off")
            # PLOT COLORED BARS TO THE AXES
            barkw = dict( color=color_label_list, linewidth=0.50, ec="k", clip_on=False, align='edge',)
            # bottom bar #
            axb.bar(labels[:,0]-.5,np.ones(len(labels)), 
                    width=np.diff(labels, axis=1).flatten(), **barkw)
            # side bar #
            axl.barh(labels[:,0]-.5,np.ones(len(labels)), 
                    height=np.diff(labels, axis=1).flatten(), **barkw)
            # SET MARGINS TO ZERO AGAIN
            ax.margins(0)
            ax.tick_params(axis="both", bottom=0, left=0, labelbottom=0,labelleft=0)
            # ADD TEXT IN THE COLOR BARS #
            for idx,x in enumerate(labels):
                align = (x[0] + x[1])/2
                axb.text(align,.5,names_abbrev[idx], fontsize=3, rotation=90, horizontalalignment='center', verticalalignment='center', weight='bold',
                        path_effects=[PathEffects.withStroke(linewidth=.5, foreground="w")])
                axl.text(.5,align,names_abbrev[idx], fontsize=3, horizontalalignment='center', verticalalignment='center', weight='bold',
                        path_effects=[PathEffects.withStroke(linewidth=.5, foreground="w")])            
            plt.savefig(os.path.join(args.outdir,f'{subid}_True_Data_{min_marker}minutes.png'), dpi=1200, format='png', bbox_inches='tight')
            # CLEAR FIGURE #
            plt.clf()
            plt.cla()
            plt.close()

def get_corrs(true_data_zmat,test_data, max_minutes, all_data_dict, TR, subid):
        times = list(range(5, (max_minutes+1), 5))  # Vector of times to plot reliability
        if times in all_data_dict['all_times']:
            pass
        else:
            all_data_dict['all_times'].append(times)
        # corr list to populate
        corr_value_list = []
        for t in times:
            time_str = str(t)
            #print(time_str)
            time_frames = math.ceil((t*60)/TR)
            # choose a random starting point at least time_frames from the end
            # available starting points without going over end of available data
            start_range = range(0, test_data.shape[1] - time_frames, 1)
            start_point = random.choice(start_range)
            #print(start_point)

            # grab the correct amount of data as new array
            sample_data = test_data[:, start_point:(start_point+time_frames)]


            ### below added to quickly make 5,10,15,and 20 min matrices for talk - DVD
            # if t == 20:
            #     ### delete after testing
            #     print(sample_data.shape)
            #     print(TR)
            #     new_shape = (333, 1084)
            #     sample_data = sample_data[:, :new_shape[1]]
            #     plot_corrs(sample_data,'20min')
            #     sys.exit()


            #print(sample_data.shape)

            # compute SAMPLE correlation and z transform
            # logger.debug('Creating SAMPLE Data Matrix...')
            sample_data_mat = np.corrcoef(sample_data)
            # replace diag 1 with 0 for z transform (just to remove inf with 0)
            np.fill_diagonal(sample_data_mat,0)
            # z transformed connectivity mat
            sample_data_zmat = np.arctanh(sample_data_mat)
            # put 1's back on the diag
            np.fill_diagonal(sample_data_zmat,1)
            # Correlate true data matrix with sample data matrix
            sample_corr = np.corrcoef(true_data_zmat.flatten(), sample_data_zmat.flatten())[0, 1]
            corr_value_list.append(sample_corr)
            #print(f'Correlation coefficient for {t}min:', sample_corr)
        # all_data_dict['all_corrs'].append(corr_value_list)
        all_data_dict[subid].append(corr_value_list)
        return all_data_dict, corr_value_list


def clean_dict(all_data_dict):
        # Get the length of the longest list in all_times
        max_length = max(len(lst) for lst in all_data_dict['all_times'])
        longest_time_idx = all_data_dict['all_times'].index(max(all_data_dict['all_times'], key=len))
        all_data_dict['all_times'] = all_data_dict['all_times'][longest_time_idx]
        # make plot-ready variables in dict
        cleaned_ids = []
        cleaned_corrs = []
        for key in all_data_dict.keys():
            if key == 'all_times':
                pass
            else:
                # add subid to the claned list
                cleaned_ids.append(key)
                # average participant's iteration correlations
                average_list = [sum(items) / len(all_data_dict[key]) for items in zip(*all_data_dict[key])]
                cleaned_corrs.append(average_list)
        # add to main dict for plotting
        all_data_dict['all_ids'] = cleaned_ids
        all_data_dict['all_corrs'] = cleaned_corrs
        #print(all_data_dict['all_ids'])
        #print(all_data_dict['all_times'])
        #print(all_data_dict['all_corrs'])
        return all_data_dict

def plot_final(all_data_dict, outdir, subid, truetime, fd_thresh, rands, num_of_sessions, subids):
        corr_value_lists = all_data_dict['all_corrs']
        labels = all_data_dict['all_ids']
        times = all_data_dict['all_times']

        # Set up list of colors from the Set2 map, based on # of subs and alpha
        colors = list(Set2.colors)
        colormap = tab20
        grp_idx = 'random'
        color_idx = -1
        plot_alpha = 0.8

        # Plot each corr list with a different color and connected dots
        fig, ax = plt.subplots(figsize=(14, 5))
        for i in range(len(corr_value_lists)):
            corr_values = corr_value_lists[i]
            # Plot all data points for the current correlation list
            plt.plot(times[:len(corr_values)], corr_values,
                    # color=next(colors),
                    color = colors[i],
                    marker='o', markersize=3,
                    linestyle='-', linewidth=2,
                    alpha=plot_alpha, label=labels[i])

            # Add black outline around points with correlation coefficients greater than or equal to 0.9
            for j, corr_value in enumerate(corr_values):
                if corr_value >= 0.9:
                    plt.plot(times[j], corr_value,
                            color='black',
                            marker='o', markersize=3.5,
                            label=None, markeredgecolor='black', markerfacecolor='none')

        # axis labels, limits, and title
        ax.set_ylim([0, 1])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_xticks(times)
        ax.set_xlabel('Scan Time (min)')
        ax.set_ylabel('Correlation Coefficient')
        ax.set_title(f'Reliability by Sample Time ({truetime} min True | {rands} Iter.)')

        # figure out legend
        n_cols = np.ceil(len(subids)/10).astype(int)
        if len(subids) <= 10:
            font_size = 'medium'
        elif len(subids) <= 20:
            font_size = 'small'
        elif len(subids) <= 30:
            font_size = 'x-small'
        elif nlen(subids) > 30:
            font_size = 'xx-small'
        ax.legend(ncol=n_cols, fontsize=font_size, loc='lower right')

        # save out file
        plt.savefig(os.path.join(outdir,f'{subid}_reliability_true{truetime}min_{fd_thresh}FD_nocontig_{num_of_sessions}visits_{rands}_Iterations.png'), dpi=1200, format='png', bbox_inches='tight')


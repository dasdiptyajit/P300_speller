#!/usr/bin/env python3
# -*- coding: utf-8 -*
# Created on April 27, 2024
"""
@author: Diptyajit Das <bmedasdiptyajit@gmail.com>
         Heidelberg, Germany
"""


# Load some basic packages
# ---------------------------------
import mne
from mne.io import Raw
from os.path import join, basename
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
# ---------------------------------


def set_directory(path=None):
    """
    info: check whether the directory exits, if no, create the directory
    :param path: the target directory.
    """
    # import necessary modules
    import os
    # ---------------------------------
    # code:
    isexists = os.path.exists(path)
    if not isexists:
        os.makedirs(path)
    return


def create_readme(subjects_dir=None, ids=None, filename=None, write_info=True):
    """
    use: create a text file with information about file structure
    :param subjects_dir:
    :param filename:
    :param write_info:
    :return:
    """

    # file directory
    fname = join(subjects_dir, filename)

    # add the information to the text file

    if write_info:
        txt = ['\n']
        txt.append('>>>>>>>>>>> information:  P3 Visual readme file <<<<<<<<<<<<<<\n')
        txt.append('@author: Diptyajit Das <bmedasdiptyajit@gmail.com>\n')
        txt.append('===================================================================\n')
        txt.append('subjects ids in this study:  %s \n' %ids)
        txt.append('add text \n')
        txt.append('add text \n')
        txt.append('===================================================================\n')
        fid = open(fname, "w")
        fid.writelines(txt)
        fid.close()


# main function -->
# -------------------------------------------------------
if __name__ == '__main__':

    # ----------------------
    # Define path parameters
    # ----------------------
    from os.path import join
    import os

    root_dir = join('/', 'Users', 'diptyajit.das', 'Documents')
    subjects_dir = join(root_dir, 'p300', '')

    # subject ids
    ids = ['S1', 'S2', 'S3', 'S4', 'S5']

    # -------------------------------
    # function parameters
    # -------------------------------

    # filter parameters in Hz
    fl_low, fl_high = 1., 30.                          # fl_low: high cutoff frequency, fl_high: low cutoff frequency

    # ICA parameters
    eeg_com = 30                                       # no. of ica components for eeg signals

    # evoked grand plot condition
    conditions = ['target', 'non-target']

    # --------------------------------------------
    # generate a readme file about file structure information
    do_create_readme_txt = False

    if do_create_readme_txt:
        write_info = True  # if true, generate a file
        filename = 'README.txt'
        create_readme(ids=ids, subjects_dir=subjects_dir, filename=filename, write_info=write_info)


    # ---------------------------------------------
    # List of steps to be performed in the pipeline
    # ---------------------------------------------
    do_preprocess_eeg_data = True                          # 1. dpreprocess eeg data  ------------> function call


    # ---------------------------------------------
    # Main section pipeline
    # ---------------------------------------------
    # loop over the subject list
    for id in ids:

        # set a new preprocessing directory for eeg data
        prep_folder = join(subjects_dir, 'eeg_preprocessing', '')
        set_directory(prep_folder)

        # set a new result directory for eeg data
        result_folder = join(prep_folder, 'plot', '')
        set_directory(result_folder)

        # -----------------------------------
        # 1. Set the EEG montage in raw object
        if do_preprocess_eeg_data:
            # load .mat data
            fname = join(subjects_dir, id + '.mat')
            mat_head = sio.loadmat(fname)

            # sampling frequency
            sfreq = mat_head['fs'] [0,0]
            # eeg channel data
            ch_data = mat_head['y']
            # extract events
            events =  mat_head['trig']

            # create a structure for mne
            ch_names = ['Fz', 'Cz', 'P3', 'Pz', 'P4', 'PO7', 'Oz','PO8']
            ch_types = ['eeg'] * ch_data.shape[1]
            info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
            info.set_montage('standard_1020')
            info['description'] = 'P300 speller dataset'

            # create raw object
            eeg_raw = mne.io.RawArray(ch_data.T, info)

            # apply a filter [fl_low, fl_high = 1., 30.]
            eeg_raw_filt = eeg_raw.copy(). filter(fl_low, fl_high, fir_design='firwin')

            # plot raw
            eeg_raw_filt.plot(scalings='auto', title='eeg raw data', block=True)

            # extract events
            events = mne.find_events(eeg_raw_filt, shortest_event=0, stim_channel=None)

            # plot the sensor configuration to check if it's correct
            fig = eeg_raw.plot_sensors(ch_type='eeg', show_names=True, show=False)
            fig.set_size_inches(16, 12)  # set the size of the figure
            fig_out = join(result_folder, '%s-montage.png' % id)
            plt.savefig(fig_out, format='png', dpi=400)

            # make a figure for events
            event_dict = {'target': 1, 'non_target': -1}
            fig = mne.viz.plot_events(events, sfreq=eeg_raw.info['sfreq'],
                                      first_samp=eeg_raw.first_samp, event_id=event_dict, show=False)
            fig.subplots_adjust(right=0.7)  # make room for legend
            fig.set_size_inches(20, 9)  # set the size of the figure
            fig_out = join(result_folder, '%s-events-%s.png' % (id, seg))
            plt.savefig(fig_out, format='png', dpi=400)


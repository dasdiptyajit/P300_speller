import numpy as np
import scipy.io as sio
import mne
import matplotlib.pyplot as plt
from mne import Epochs, pick_types

# Define functions for loading data, preprocessing, and artifact rejection

def load_data(file_path):
    mat_data = sio.loadmat(file_path)
    fs = mat_data['fs'][0, 0]  # Sampling frequency
    y = mat_data['y']  # EEG data
    trig = mat_data['trig'][:, 0]  # Ensure trig is 1D
    return y, trig, fs

def preprocess_eeg_data(y, trig, fs):
    ch_names = ['Fz', 'Cz', 'P3', 'Pz', 'P4', 'PO7', 'Oz', 'PO8']
    ch_types = ['eeg'] * len(ch_names)
    info = mne.create_info(ch_names=ch_names, sfreq=fs, ch_types=ch_types)
    info.set_montage('standard_1020')
    raw = mne.io.RawArray(y.T, info)
    # set the average reference
    raw.set_eeg_reference('average', projection=False)
    raw.filter(1., 30., fir_design='firwin')
    return raw, trig

def plot_full_trigger_data(trig):
    plt.figure(figsize=(15, 5))
    plt.plot(trig, label='Trigger Signal')
    plt.title('Full Trigger Channel Data')
    plt.xlabel('Samples')
    plt.ylabel('Trigger Value')
    plt.legend()
    plt.show()

def reject_parameter(raw, events):
    picks = pick_types(raw.info, meg=True, eeg=True, stim=False)
    # Define event IDs
    event_id = {'non-target': -1, 'target': 1}
    dummy_epochs = mne.Epochs(raw, events, event_id=event_id, tmin=-0.1, tmax=1.0,
                     picks=picks, baseline=(None, 0), preload=True,
                     reject=None)

    from autoreject import get_rejection_threshold  # noqa
    reject = get_rejection_threshold(dummy_epochs)
    return reject


# Load and preprocess the data
file_path = '/Users/diptyajit.das/Documents/p300/S4.mat'
y, trig, fs = load_data(file_path)
raw, trig = preprocess_eeg_data(y, trig, fs)

# Manually create events array from the cleaned triggers
event_times = np.where(np.diff(trig) != 0)[0] + 1  # Find changes in trigger values
event_values = trig[event_times]  # Get the trigger values at these times
events = np.column_stack((event_times, np.zeros_like(event_times), event_values))

# Plot full trigger data to understand its behavior
plot_full_trigger_data(trig)

# Define event IDs
event_id = {'non-target': -1, 'target': 1}

# Plot full trigger events for targets and non-targets
fig = mne.viz.plot_events(events, sfreq=raw.info["sfreq"], first_samp=raw.first_samp, event_id=event_id)

# Create epochs for ERP analysis
epochs = mne.Epochs(raw, events, event_id=event_id, tmin=-0.1, tmax=0.8, baseline=(None, 0), preload=True)

# get reject parameter
reject = reject_parameter(raw, events)
cleaned_epochs = epochs.drop_bad(reject)

evoked_trg = cleaned_epochs['target'].average()
evoked_nontrg = cleaned_epochs['non-target'].average()

evoked_trg.plot()
evoked_nontrg.plot()

# Plot the Power Spectral Density components
psd_fig = cleaned_epochs['target'].plot_psd(show=True)
plt.show()

from ovation.conversion import iterable
from ovation.data import as_data_frame

import scipy as sp

def calculate_cell_means(project):
    cells = {}
    epochs = []
    for expt in iterable(project.getExperiments()):
        for epoch in iterable(expt.getEpochs()): # ctx.getObjectsWithTag('demo')
            epochs += [epoch]
            cell = epoch.getInputSources().get('cell')
            if len(list(iterable(epoch.getMeasurements()))) > 0:
                m = epoch.getMeasurement('Membrane current')
                data = as_data_frame(m)
                peak = max(data['current']).item()
                k = "{0} ({1})  {2}".format(cell.getLabel(), cell.getIdentifier(), cell.getURI().toString())
                peaks = cells.get(k, {})
                pk = "{0} mV".format(epoch.getProtocolParameters().get('step_amplitude_mV'))
                cell_peaks = peaks.get(pk, [])
                peaks[pk] = cell_peaks + [peak]
                cells[k] = peaks
    
    for (k,v) in cells.iteritems():
        for ck, cv in v.iteritems():
            v[ck] = sp.mean(cv)
    
        cells[k] = v
        
    return (cells, epochs)
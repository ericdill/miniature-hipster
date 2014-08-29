__author__ = 'edill'


from pyspec.spec import SpecDataFile, FileProcessor
from matplotlib import pyplot
import numpy as np
import sys
from metadataStore.userapi.commands import create, record
from time import mktime
from datetime import datetime

spec_folder_path = "c:\\DATA\\X1A2\\X1Data\\"
spec_folder_path = "/home/edill/X1Data/"
spec_file_name = spec_folder_path + "LSCO_Oct13"
ccd_path = spec_folder_path + "LSCO_Oct13_spec_img/"
numpy_path = spec_folder_path + "LSCO_Oct13_numpy/"
broker_path = spec_folder_path + "LSCO_Oct13_broker/"
output_images = True

sf = SpecDataFile(spec_file_name, ccdpath=ccd_path)

epics_to_unix_time_delta = 1373565155

scan_nos = range(387, 469)
dont_include = [400, 401, 403, range(424, 449), 451, ]
flat_list = []
for item in dont_include:
    if isinstance(item, list):
        for bar in item:
            flat_list.append(bar)
    else:
        flat_list.append(item)

dont_include = flat_list

for num in dont_include:
    index = scan_nos.index(num)
    scan_nos.pop(index)

motors = []
images = []
temp = []
wavelength = []
ub = []
img_files=[]
data_keys = ['wavelength', 'motors', 'img', 'sample temperature', 'ub']
# scan_nos = [388]
for scan_no in scan_nos:
    temp = sf[scan_no].Tsam
    motors = sf[scan_no].getSIXCAngles()
    wavelength = sf[scan_no].wavelength
    ub = sf[scan_no].UB.tolist()
    time = datetime.fromtimestamp(mktime(sf[scan_no].scandate))

    det_size = 256
    pix_size = 0.0135*2048/det_size
    beamline_config = {'scan_id': scan_no,
                       'config_params': {
                           'pixel_size': (pix_size, pix_size),
                           'calibrated_center': (det_size/2, det_size/2),
                           'dist_sample': 355.0,
                           'wavelength': wavelength
                       }}

    create(header={'scan_id': scan_no})
    create(beamline_config=beamline_config)
    create(event_descriptor={'scan_id': scan_no,
                             'descriptor_name': 'hkl_scan',
                             'event_type_id': 1,
                             'tag': 'experimental',
                             'data_labels': data_keys})

    scan = sf[scan_no]
    fp = FileProcessor(spec=scan)
    fp.process()
    image_stack = fp.getImage()
    fnames = []

    dt_scan_start = datetime.fromtimestamp(mktime(scan.scandate))
    dt_first_frame = datetime.fromtimestamp(scan.Epoch[0])
    frame_times = [(datetime.fromtimestamp(_) - dt_first_frame) + dt_scan_start
                   for _ in scan.Epoch]
    for idx in range(image_stack.shape[0]):
        file = (numpy_path+"scan_"+str(scan_no)+"_img_"+str(idx))
        fnames.append(file)
        np.save(file=file, arr=image_stack[idx])

        curtemp = temp[idx]
        curmotors = motors[idx].tolist()
        curwavelength = wavelength
        curub = ub
        time = frame_times[idx]
        # print("file: {0}, type: {1}".format(file, file.__class__))
        # print("sample temperature: {0}, type: {1}".format(curtemp,
        #                                                   curtemp.__class__))
        # print("ub: {0}, type: {1}".format(curub, curub.__class__))
        # print("motors: {0}, type: {1}".format(curmotors,
        #                                       curmotors.__class__))
        # print("wavelength: {0}, type: {1}".format(curwavelength,
        #                                           curwavelength.__class__))
        record(scan_id=scan_no, descriptor_name='hkl_scan', seq_no=idx,
               data={'img': file,
                     'sample temperature': curtemp,
                     'ub': curub,
                     'motors': curmotors,
                     'wavelength': curwavelength,
                     'time': time})
    img_files.append(fnames)

print("wavelength: {0}".format(wavelength))
for idx, (T) in enumerate(temp):
    print("scan number {0}: avg T: {1}".format(scan_nos[idx], np.average(T)))
temps = [item for sublist in temp for item in sublist]
pyplot.plot(temps)
pyplot.show()
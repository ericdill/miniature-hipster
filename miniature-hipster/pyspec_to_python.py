__author__ = 'edill'


from pyspec.spec import SpecDataFile, FileProcessor
from matplotlib import pyplot
import numpy as np
import sys
# from metadataStore.userapi.commands import create, log

spec_folder_path = "c:\\DATA\\X1A2\\X1Data\\"
# spec_folder_path = "/home/edill/X1Data/"
spec_file_name = spec_folder_path + "LSCO_Oct13"
ccd_path = spec_folder_path + "LSCO_Oct13_spec_img/"
numpy_path = spec_folder_path + "LSCO_Oct13_numpy/"
broker_path = spec_folder_path + "LSCO_Oct13_broker/"
output_images = True

sf = SpecDataFile(spec_file_name, ccdpath=ccd_path)

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
for scan_no in scan_nos:
    temp.append(sf[scan_no].Tsam)
    motors.append(sf[scan_no].getSIXCAngles())
    wavelength.append(sf[scan_no].wavelength)
    ub.append(sf[scan_no].UB)
    if output_images:
        spec_scan = sf[scan_no]
        fp = FileProcessor(spec=spec_scan)
        fp.process()
        image_stack = fp.getImage()
        fnames = []
        for idx in range(image_stack.shape[0]):
            file = (numpy_path+"scan_"+str(scan_no)+"_img_"+str(idx))
            fnames.append(file)
            np.save(file=file, arr=image_stack[idx])
        img_files.append(fnames)

np.save(file=broker_path+"motors", arr=motors)
np.save(file=broker_path+"temp", arr=temp)
np.save(file=broker_path+"wavelength", arr=wavelength)
np.save(file=broker_path+"ub", arr=ub)

print("wavelength: {0}".format(wavelength))
for idx, (T) in enumerate(temp):
    print("scan number {0}: avg T: {1}".format(scan_nos[idx], np.average(T)))
temps = [item for sublist in temp for item in sublist]
pyplot.plot(temps)
pyplot.show()
import csv, sys, json, io
#System dependencies (write_binaryFile)
import shutil
#System dependencies (compressed files)
import zipfile, gzip, bz2, tarfile

class base_exportData():
    """a class to export data"""

    def __init__(self,data_I=[]):
        if data_I: self.add_data(data_I);
        else: self.data = [];

    def add_data(self,data_I):
        """add data"""
        self.data = data_I;

    def clear_data(self):
        """clear existing data"""
        #del self.data[:];
        self.data = None;

    def write_dict2csv(self,filename,headers=None):
        # write dict to csv
        with open(filename, 'w',newline='') as f:
            if headers: fieldname = headers;
            else: fieldname = list(self.data[0].keys())
            writer = csv.DictWriter(f, fieldnames = fieldname)
            try:
                writer.writeheader();
                writer.writerows(self.data);
            except csv.Error as e:
                sys.exit(e);

    def write_dict2json(self,filename):
        # write dict to json file
        with open(filename, 'w',newline='') as outfile:
            json.dump(self.data, outfile, indent=4);

    def write_dict2tsv(self,filename):
        # write dict to tsv
        with open(filename, 'w',newline='') as f:
            writer = csv.DictWriter(f,fieldnames = list(self.data[0].keys()),dialect = 'excel-tab')
            try:
                writer.writeheader();
                writer.writerows(self.data);
            except csv.Error as e:
                sys.exit(e);

    def write_headerAndColumnsAndElements2csv(self,header_I,columns_I,filename):
        # make header
        header = [''];
        header.extend(header_I);
        # make rows
        rows = self.data;
        for i in range(len(columns_I)):
            rows[i].insert(0,columns_I[i]);

        with open(filename, 'w',newline='') as f:
            writer = csv.writer(f);
            try:
                writer.writerow(header);
                writer.writerows(rows);
            except csv.Error as e:
                sys.exit(e);

    def write_headersAndElements2csv(self,header_I,filename):
        # write data to csv file
        with open(filename, 'w',newline='') as f:
            writer = csv.writer(f);
            try:
                writer.writerows(header_I);
                writer.writerows(self.data);
            except csv.Error as e:
                sys.exit(e);

    def write_headersAndElements2txt(self,header_I,filename):
        # write data to txt file
        with open(filename, 'w',newline='') as f:
            writer = csv.writer(f, delimiter='\t');
            try:
                writer.writerows(header_I);
                writer.writerows(self.data);
            except csv.Error as e:
                sys.exit(e);

    def write_dict2js(self,filename,varname):
        # write dict to js file
        json_str = 'var ' + varname + ' = ' + json.dumps(self.data);
        with open(filename,'w') as file:
            file.write(json_str);

    def write_binaryFile(self,filename,length=131072):
        '''Write a binary file stream to disk
        INPUT:
        filename = string
        self.data = binary file stream
        length = chunks of memory to write to disk
        '''
        ##write from the start of the file
        #file.seek(0)
        if type(self.data)==type(b''):
            data = io.BytesIO(self.data)
        elif type(self.data)==type(io.BytesIO()):
            data = self.data;
        with open(filename,mode='wb') as f:
            shutil.copyfileobj(data, f, length=length)

    def write_binary2gz(self,filename,length=131072):
        '''Write a binary file stream to disk in gz compression
        INPUT:
        filename = string
        self.data = binary file stream
        length = chunks of memory to write to disk
        '''
        with gzip.open(filename, 'wb') as f:
            shutil.copyfileobj(self.data, f, length=length)

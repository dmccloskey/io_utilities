from .base_importData import base_importData
import zipfile
#System dependences (get_request)
import requests, sys
#System dependencies (ftp)
from ftplib import FTP
import io

class import_webData(base_importData):
    def decode_request(
        self,
        request_I):
        ''' 
        decode request
        INPUT:
        request_I
        OUTPUT:
        decoded = decoded request object
        EXAMPLE:
        decoded = decode_request(request_I)
        '''

        decoded = None;
        #parse based on the headers
        if 'text/plain' in request_I.headers["Content-Type"]:
            decoded = request_I.text;
        elif "application/json" in request_I.headers["Content-Type"]:
            decoded = request_I.json()
        elif 'binary' in request_I.headers["Content-Type"]:
            decoded = request_I.content
        return decoded;
    def get_request(
        self,
        server,
        ext,
        request_parameters_I={},
        raise_I=False,
        verbose_I=True):
        ''' 
        get request using REST
        INPUT:
        server = string
        ext = string
        OUTPUT:
        decoded = json decoded dictionary
        EXAMPLE:
        server = "http://bigg.ucsd.edu"
        ext = "/api/v2/models/iJO1366/reactions"
        request = get_request(server,ext)
        '''
        r = requests.get(server+ext, **request_parameters_I)
        #check the status code
        if verbose_I: print("request status code " + str(r.status_code))
        if not r.ok:
            if raise_I: r.raise_for_status();
            return None;
        #check the encoding
        if verbose_I: print(r.encoding);
        return r;
    def parse_textRequest(
        self,
        request,
        iter_lines_parameters_I = {},
        encoding = 'utf-8',
        deliminator = '\t',
        newline = '\n',
        headers = [],
        n_lines_metadata = 0):
        '''
        Parse a binary file
        INPUT:
        file = binary file
        encoding = string, encoding type
        deliminator = string, column deliminator
        newline = string, new line deliminator
        headers = list, list of headers
            if headers = [], first row will be treated as the keys build the dictionary
        n_lines_metadata = integer, number of metadata lines to skip
        OUTPUT:
        rows_O = [{}] of parsed and decoded elements
        '''
        rows_O = [];
        cnt = 0;
        for line in request.iter_lines(decode_unicode=True,delimiter=newline,**iter_lines_parameters_I):
            #check for metadata
            if cnt<n_lines_metadata:
                cnt+=1;
                continue;
            #parse data                
            #print(text)
            row = line.split(deliminator)
            #print(row)
            #check for headers
            if not headers:
                headers = row;
            else:
                rows_O.append(dict(zip(headers, row)))
        request.close();
        return rows_O;

    def access_ftp(self,server,username=None,password=None):
        ''' 
        access ftp server
        INPUT:
        server = string
        username = string
        password = string
        OUTPUT:
        ftp = FTP object
        EXAMPLE:
        '''
    
        #domain name or server ip:
        ftp = FTP(server)
        ftp.login(user = username, passwd = password)
        return ftp;
    def get_ftp(
        self,server,ext,filename,username=None,password=None):
        '''
        get ftp file from ftp server
        INPUT:
        server = string
        ext = string
        filename = string
        username = string
        password = string
        OUTPUT:
        ftp = FTP object
        EXAMPLE:
        server = "ftp.ebi.ac.uk"
        ext = "/pub/databases/chebi/Flat_file_tab_delimited/"
        filename = "chebiId_inchi_3star.tsv"
        file = get_ftp(server,ext,filename)
        '''
    
        ftp = self.access_ftp(server,username=username,password=username)
        #change directory:
        ftp.cwd(ext)
        #download the file
        sio = io.BytesIO()
        def handle_binary(more_data):
            sio.write(more_data)
        ftp.retrbinary('RETR ' + filename, callback=handle_binary)
        sio.seek(0)
        ftp.quit()
        return sio;
    def post_ftp(self,server,ext,filename,username=None,password=None):
        '''
        post ftp file to ftp server
        INPUT:
        server = string
        ext = string
        filename = string
        username = string
        password = string
        OUTPUT:
        ftp = FTP object
        EXAMPLE:
        server = "ftp.ebi.ac.uk"
        ext = "/pub/databases/chebi/Flat_file_tab_delimited/"
        filename = "chebiId_inchi_3star.tsv"
        file = get_ftp(server,ext,filename)
        '''
    
        ftp = self.access_ftp(server,username=username,password=username)
        #change directory:
        ftp.cwd(ext)
        #upload the file
        ftp.storbinary('STOR '+filename, open(filename, 'rb'))
        ftp.quit()

    def parse_binaryFile(
        self,
        file,
        encoding = 'utf-8',
        deliminator = '\t',
        newline = '\n',
        headers = []):
        '''
        Parse a binary file
        INPUT:
        file = binary file
        encoding = string, encoding type
        deliminator = string, column deliminator
        newline = string, new line deliminator
        headers = list, list of headers
            if headers = [], first row will be treated as the keys build the dictionary
        OUTPUT:
        rows_O = [{}] of parsed and decoded elements
        '''
        rows_O = [];
        for line in iter(file.readline, ''.encode(encoding)):
            #parse data
            text = line.decode(encoding)
            if text=='':
                print(text)
                break;
            #print(text)
            row = text.replace(newline,'').split(deliminator)
            #print(row)
            #check for headers
            if not headers:
                headers = row;
            else:
                rows_O.append(dict(zip(headers, row)))
        return rows_O;
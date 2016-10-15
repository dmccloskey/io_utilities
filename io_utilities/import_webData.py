from .base_importData import base_importData
#System dependences (get_request)
import requests, sys
#System dependencies (ftp)
from ftplib import FTP
import io

class import_webData(base_importData):
    def get_request(
        self,
        server,
        ext):
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
        decoded = get_request(server,ext)
        '''
        decoded = None;
        r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
        if not r.ok:
    #         r.raise_for_status()
            pass
        else:
            decoded = r.json()
        return decoded
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
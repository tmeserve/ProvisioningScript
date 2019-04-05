import ftplib
ftp = ftplib.FTP('ftp.cphandheld.com', 'provisioning', 'ProvFtp$')

file = open("/Users/tylermeserve/Documents/VectorConfigUtility/Testing/Test2/cfgmdm/uploadFiles/41000532-20190404-165907.config.txt", 'rb')

ftp.storbinary("STOR test.config.txt", file)
file.close()
ftp.close()
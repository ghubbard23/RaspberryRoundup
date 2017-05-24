import os
import sys
import subprocess
import time
import code128
import datetime
import os.path

#time.sleep(60)

def ping():
    print('Checking for response from file server...')
    #ip of file server
    ip = "192.168.255.46"
    response = os.system("ping -c 4 " + ip)
    if response == 0:
        print(ip , 'is reachable')
        print("\n")
        return ip
    else:
        print(ip , 'is unreachable.')

def getserial():
    print('Getting Serial info...')
    #need to add check to make sure the serial actually was grabbed
    cpuinfo=subprocess.Popen("cat /proc/cpuinfo | grep Serial | cut -d' ' -f2", stdout=subprocess.PIPE, shell=True)
    output_bytes, err = cpuinfo.communicate()
    output_string = str(output_bytes, 'utf-8')
    output_string = output_string.strip('\n')
    print('Serial Number is: ' + output_string)
    print("\n")
    return output_string
    
def getmacaddr():
    print('Getting MAC Address...')
    #need to add check to make sure the macaddr actually was grabbed
    ifconfig=subprocess.Popen("ifconfig eth0 | grep HWaddr |cut -dH -f2|cut -d\  -f2", stdout=subprocess.PIPE, shell=True)
    if_output_bytes, err = ifconfig.communicate()
    if_output_string = str(if_output_bytes, 'utf-8')
    if_output_string = if_output_string.rstrip('\n')
    print('MAC Address is: ' + if_output_string)
    print("\n")
    return if_output_string

def is_mount(ip):
    print('Mounting Network Drive...')
    print('Checking to make sure network drive is mounted...')
    #what the mount point should look like
    subprocess.Popen("sudo mount -a", stdout=subprocess.PIPE, shell=True)
    time.sleep(5)
    mount_should="//%s/Folder" % ip
    mount_point=subprocess.Popen("df | grep Folder | cut -d\  -f1", stdout=subprocess.PIPE, shell=True)
    mount_output_bytes, err = mount_point.communicate()
    mount_output_string = str(mount_output_bytes, 'utf-8')
    #removes line break after mount point
    mount_output_string = mount_output_string.rstrip('\n')
    if mount_output_string == mount_should:
        print(mount_output_string + " is mounted")
        print("\n")
    else:
        input(mount_should + " not mounted. Check network cables and press any key to exit: ")
        sys.exit()
            
    return mount_output_string

def asset_tag():
    try:
        tag_number1 = int(input("Please type asset tag number: "))
    except:
        input("Something is wrong with your input. Press Enter to restart the script. :")
        return asset_tag()
    #empty check is handlded by the integer input. Empty space is not an integer
    tag_number2 = int(input("Please retype Asset tag number: "))
    if str(tag_number1) == str(tag_number2):
        #if os.path.isdir("/home/pi/Desktop/SharedFolder/%d" % tag_number1):
        #    print('Your asset tag number has already been used. Please try again.')
        #    return asset_tag()
        tag_number=tag_number1
        print("Asset tag number is %d" % tag_number)
        print("\n")
        return tag_number
    else:
        input("Asset tag numbers did not match. Press Enter to try the Asset Tag again. :")
        return asset_tag()

def create_text_file(tag_number, serial, macaddr):
    print('Creating QA File with Asset, Serial and MAC info...\n')
    #the goal is to create a folder named as the asset tag # and store all supporting documentation within that folder
    os.makedirs("/home/pi/Desktop/SharedFolder/%d" % tag_number, exist_ok=True)
    file=open("/home/pi/Desktop/SharedFolder/%d/%d.txt" % (tag_number, tag_number), "w")
    file.write("Asset Tag number: %d\r\n" % tag_number)
    file.write("Serial: %s\r\n" % serial)
    file.write("MAC Address: %s\r\n" % macaddr)
    file.write('%s\n' % (datetime.datetime.now()))
    file.close()
    print('QA File created!')
    time.sleep(2)
    print('Checking to make sure QA file was created correctly')
    if os.path.isfile("/home/pi/Desktop/SharedFolder/%d/%d.txt" % (tag_number, tag_number)):
        print("QA File was created correctly")
        print("\n")


def test_code128_barcode_gen(tag_number, serial, macaddr):
    print("Generating barcode for MAC Address...")
    time.sleep(2)
    code128.image("%s" % macaddr).save("/home/pi/Desktop/SharedFolder/%d/MAC Address - %s.png" % (tag_number, macaddr))  # with PIL present
    print("Generating barcode for Serial Number...")
    print("\n")
    time.sleep(2)
    code128.image("%s" % serial).save("/home/pi/Desktop/SharedFolder/%d/Serial - %s.png" % (tag_number, serial))
    with open("/home/pi/Desktop/SharedFolder/%d.svg" % tag_number , "w") as f:
        f.write(code128.svg("%s" % macaddr))
    print("Checking to make sure Barcode files were saved correctly...")
    if os.path.isfile("/home/pi/Desktop/SharedFolder/%d/MAC Address - %s.png" % (tag_number, macaddr)):
        print("MAC address barcode was created correctly!")
    else:
        print("Couldn't find file.")
    if os.path.isfile("/home/pi/Desktop/SharedFolder/%d/Serial - %s.png" % (tag_number, serial)):
        print("Serial barcode was created correctly!")
    else:
        print("Couldn't find file.")
    

def main():
    ip=ping()
    is_mount(ip)
    tag_number=asset_tag()
#    duplicate_asset_tag(tag_number)
    serial=getserial()
    macaddr=getmacaddr()
    create_text_file(tag_number, serial, macaddr)
    test_code128_barcode_gen(tag_number, serial, macaddr)
    input("Script Finished. Please check the file server to make sure the QA file, and barcodes were generated correctly. Press Enter to exit script.")



main()
    





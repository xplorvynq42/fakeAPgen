import subprocess
import optparse
import time

def showBanner():
    try:
        with open("banner.txt" , "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("Banner file not found")

def parseArguments():
    parser = optparse.OptionParser()

    parser.add_option("-e", "--essid", dest="essid", help="SSID of the Fake AP")
    parser.add_option("-i", "--interface", dest="interface", help="Interface to use")
    parser.add_option("-c", "--count", dest="count", type="int", help="How many fake APs to generate")

    (options, args) = parser.parse_args()
    if not options.essid or not options.interface or not options.count:
        parser.error("You must specify -e (essid), -i (interface) , and -c (count)")

    return options.essid,options.interface,options.count


def startFakeAP(essid,interface,count):
    processes = []
    for num in range(count):
        ssid = f"{essid}_{num+1}"
        p = subprocess.Popen(
            ["/usr/sbin/airbase-ng","--essid",ssid,interface],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        processes.append(p)
        print(f"Fake AP Started:{ssid} ")
        time.sleep(1)
    return processes


def stopFakeAP(processes):
    print("Stopping all Fake APs...")
    for p in processes:
        p.terminate()
    print("All processes terminated. Exiting")


def main():
    showBanner()
    print("Phantom Attack Started")
    essid,interface,count = parseArguments()
    processes = startFakeAP(essid,interface,count)
    print("All fake APs generated, press CTRL + C to stop Phantom Attack")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stopFakeAP(processes)

if __name__ == "__main__":
    main()
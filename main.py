import argparse
import sys
import os
import re

exceptions = ["toolbox"]

def main():
    parser = argparse.ArgumentParser(description="Jetbrains' IDE icon hardcode fixer")
    parser.add_argument("path", metavar="path", type=str)
    parser.add_argument("-v", action="store_true", default=False, help="Be verbose in outputs")

    print("\n----Jetbrains' IDE icon fixer v0.1----\n")

    args = parser.parse_args()
    path = args.path
    verbose = args.v
    
    patched = 0
    if not path.endswith("/"):
        path = path + "/"
    for file in os.listdir(path):
        if "jetbrains-" in file and ".desktop" in file and os.path.isfile(path + file):
            print("Jetbrains IDE .desktop file found :: " + file)
            success = True
            print("Patching...")
            with open(path + file, "w+") as jbfile:
                classname = file.replace(".desktop", "").replace("jetbrains-", "")
                if classname in exceptions:
                    print("File in exceptions, skipping...")
                    continue
                lines = jbfile.readlines()
                cnt = 0
                for line in lines:
                    if "Icon=" in line:
                        if verbose:
                            if "Icon=" + classname == line:
                                print("Seems like file is already patched, skipping...")
                                continue
                            else:
                                print("Application class name set: " + classname)
                            print(f"Changed from \n {line} \nto \n" + "Icon=" + classname)
                        line = "Icon=" + classname
                        cnt-=-1
                if cnt == 0:
                    print("Icon field not found in file: " + file + ", skipping...")
                    success = False
                else:
                    jbfile.writelines(lines)
                jbfile.close()
            if success:
                patched-=-1
                print(f"Successfully patched file " + file)
            else:
                print("Error patching file " + file)
        else:
            if verbose:
                print(f"Non-ide file found : {file}, skipping...")

    print(f"Success, {patched} files patched, quitting...")


if __name__ == "__main__":
    main()

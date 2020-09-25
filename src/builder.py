import PyInstaller.__main__
import os
import shutil


def main():
    PyInstaller.__main__.run(["--onefile",os.path.join(os.getcwd(),"run_game.py")])
    print("finished building...copying additional files to target directory")
    if os.path.isdir(os.path.join(os.getcwd(),"dist","data")):
        print("clearing old junk")
        shutil.rmtree(os.path.join(os.getcwd(),"dist","data"))
    shutil.copytree(src=os.path.join(os.getcwd(),"data"),dest=os.path.join(os.getcwd(),"dist","data"))
    print('\033[92m'+"ALL DONE!")

if __name__ == "__main__":
    main()
import PyInstaller.__main__
import os
import shutil



def main():
    print(os.getcwd())
    PyInstaller.__main__.run(["--onefile", os.path.join(os.getcwd(), "run_game.py")])
    print("finished building...copying additional files to target directory")
    if os.path.isdir(os.path.join(os.getcwd(), "dist", "data")):
        print("clearing old junk")
        shutil.rmtree(os.path.join(os.getcwd(), "dist", "data"))
    for file in os.listdir(os.path.join(os.getcwd(), "data", "img", "crew_faces")):
        os.unlink(os.path.join(os.getcwd(), "data", "img", "crew_faces", file))
    for file in os.listdir(os.path.join(os.getcwd(), "data", "savegame")):
        os.unlink(os.path.join(os.getcwd(), "data", "savegame", file))
    if os.path.isfile(os.path.join(os.getcwd(), "data", "other", "highscores.json")):
        os.unlink(os.path.join(os.getcwd(), "data", "other", "highscores.json"))
    shutil.copytree(src=os.path.join(os.getcwd(), "data"), dst=os.path.join(os.getcwd(), "dist", "data"))
    print("Build finished successfully")

if __name__ == "__main__":
    try:
       main()
    except Exception as e:
        print("CRITICAL ERROR! BUILD FAILED")
        print(e)

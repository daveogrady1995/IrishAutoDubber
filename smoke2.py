import traceback

mods = [
    "dubbing_core",
    "dubbing_core.core",
    "gui",
    "gui.gui_app",
    "cli",
    "cli.dub_to_irish",
    "source.gui_app",
]
for m in mods:
    try:
        __import__(m, fromlist=["*"])
        print(m + " OK")
    except Exception as e:
        print(m + " ERROR ->", e)
        traceback.print_exc()
print("done")

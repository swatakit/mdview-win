# MD Viewer

![icon](icon-preview.png)

Double-click a `.md` file on Windows and read it rendered in your browser, with tables, code blocks and Mermaid diagrams.

Made for locked-down work laptops: no Microsoft Store, no browser extension, no admin rights, nothing to install. A few small text files you can read, plus a launcher your own PC builds.

```mermaid
graph LR
    A[Double-click .md] --> B[MDViewer.exe]
    B --> C[mdview.bat]
    C --> D[mdview.py]
    D --> E[Rendered page in your browser]
```

## What you need

| Requirement | Notes |
|---|---|
| Windows 10 or 11 | Uses the C# compiler that ships with Windows to build the launcher. |
| Python | `pythonw`, `pyw` or `uv` must work from a command prompt. |
| Internet access to `cdn.jsdelivr.net` | For Mermaid diagrams. Also for rendering if the Python `markdown` package is not installed. Without it you see plain text. |

## What's in the folder

| File | What it is |
|---|---|
| `mdview.py` | Converts the Markdown file to a temporary HTML page and opens it. |
| `mdview.bat` | Finds Python and runs `mdview.py`. |
| `mdview.ico` | The icon. |
| `mdview-launcher.cs` | Source of the launcher (20 lines). It starts `mdview.bat` without a black window. |
| `build-exe.bat` | Builds `MDViewer.exe` from the source and registers it for your user. |

Everything is plain text you can open in Notepad, except the icon.

## Install (about 3 minutes)

| Step | Do this |
|---|---|
| 1 | On GitHub, click **Code > Download ZIP**, extract it, and put the folder somewhere it won't move, e.g. `C:\Users\<you>\Tools\mdview`. |
| 2 | Double-click `build-exe.bat`. Wait for "Built MDViewer.exe", then press any key. |
| 3 | Right-click any `.md` file > Open with > **Choose another app**. |
| 4 | Pick **MD Viewer**. If it isn't listed, scroll down > **Choose an app on your PC** > select `MDViewer.exe` in the folder. |
| 5 | Click **Always**. |
| 6 | Double-click a `.md` file to test. |

## If something goes wrong

| You see | What to do |
|---|---|
| "Windows protected your PC" when running `build-exe.bat` | The file came from email or chat. Right-click it > Properties > tick **Unblock** > OK, then run it again. |
| "Build failed" or "was not created or was removed" | Company policy or antivirus blocked the build. Use `mdview.bat` as the app in step 4 instead; it works the same but shows a brief black window and has no menu icon. |
| "Could not find Python" | Install Python, or make sure `pythonw` or `uv` runs from a command prompt. |
| Plain unformatted text in the browser | `cdn.jsdelivr.net` is blocked on your network. |
| Icon doesn't appear | Task Manager > Windows Explorer > Restart. |
| Edited the file but the page is unchanged | Double-click the file again. The page is a snapshot. |

## Good to know

- Your `.md` files are only read, never changed. Their content is not sent anywhere.
- The HTML pages are written to your temp folder (`%TEMP%\mdview`).
- The install only writes to this folder and to your own user profile in the registry (`HKEY_CURRENT_USER`).
- Don't move or rename the folder after installing. If you must, run `build-exe.bat` again and repeat steps 3 to 5.

## Security note

Markdown files can contain HTML and scripts, and this viewer does not strip them. Only open `.md` files you trust, as you would with any `.html` file.

## Uninstall

| Step | Do this |
|---|---|
| 1 | Right-click a `.md` file > Open with > Choose another app > pick another app (e.g. VS Code) > **Always**. |
| 2 | Open PowerShell and run the line below. |
| 3 | Delete the `mdview` folder. |

```powershell
Remove-Item 'HKCU:\Software\Classes\Applications\MDViewer.exe' -Recurse
```

## Licence

MIT. Free to use, change and share. See `LICENSE`.

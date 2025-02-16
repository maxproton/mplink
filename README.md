```
           /$$      /$$ /$$$$$$$  /$$       /$$$$$$ /$$   /$$ /$$   /$$
          | $$$    /$$$| $$__  $$| $$      |_  $$_/| $$$ | $$| $$  /$$/
          | $$$$  /$$$$| $$  \ $$| $$        | $$  | $$$$| $$| $$ /$$/ 
          | $$ $$/$$ $$| $$$$$$$/| $$        | $$  | $$ $$ $$| $$$$$/  
          | $$  $$$| $$| $$____/ | $$        | $$  | $$  $$$$| $$  $$  
          | $$\  $ | $$| $$      | $$        | $$  | $$\  $$$| $$\  $$ 
          | $$ \/  | $$| $$      | $$$$$$$$ /$$$$$$| $$ \  $$| $$ \  $$
          |__/     |__/|__/      |________/|______/|__/  \__/|__/  \__/
                                                             
                                                             
                                                             
                We take your requests and send them in all directions!                                                                           
                                                                         
                                  (c) Maxproton Labs
                            Licensed under Apache License 2.0

              Please do not use in military or for illegal purposes.
         (This is the wish of the author and non-binding. Many people working
          in these organizations do not care for laws and ethics anyways.
               You are not one of the "good" ones if you ignore this.)
```

## Overview

This tool detects dead links within a website. It takes the found links within a site map and also any links found in the inital page.
## Features

- Analyze a given site for deadlins
- Generates CSV file with dead links
- Checks for dead images as well

## Installation

Ensure you have Python installed (>=3.6). Clone this repository and navigate into the directory:

Run the install bash.

Please note!! --break-system-packages is used!
```bash
git clone https://github.com/maxproton/mplink
cd mplink
bash install.sh
```
## Usage
### Basic
```bash
python main.py --domain [domain] --verbose (optional)
```

## Licence
Licensed under Apache License 2.0
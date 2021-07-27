# PokerBot: Machine Learning Multi-Agent Simulation
## Table of contents
* [General info](#general-info)
* [Getting started](#getting-started)

<br />
<br />

## General info
This "PokerBot"-Project deals with the topic of machine learning and was written in the context of the lecture "Advanced Applied Machine Learning" in the course WWI18DSB Wirtschaftsinformatik Data Science at DHBW Mannheim. 
The contributors to this project were 
* Peter Behrens 
* Nina Mergelsberg and
* Niklas Wichter


### Objective and approach

The goal of this machine learning project is to model and implement a PokerBot. This bot is based on an algorithm for games with imperfect information, a variant of Counterfactual Regret Minimization and the Nash equilibrium. 
Furthermore, we implemented a GUI that can be used to play interactively against the bot. 

In this repository you can find both the project report [project report](Projektbericht_PokerBot.pdf) and the [final presentation](Präsentation_PokerBot.pdf). 

<br />

**Demo Video:** 

![app_demo](https://github.com/ishikota/PyPokerGUI/blob/master/screenshot/poker_demo.gif)

Source: https://github.com/ishikota/PyPokerGUI

<br />
<br />

## Getting started 
### Required programs
The required programs that have to be installed on the computer should be (see requirements.txt):
```
pip install
```

* matplotlib
* numpy
* PyPokerEngine
* PyPokerGUI (Attention there may be a conflict with Jupyter Notebook because of the version of the module tornado)

<br />

### How to set it up (This part is currently not working due to a bug in the PyPokerGUI module!)
After all required programs have been installed, the GUI can executed. 

For the next step it is important to change/adjust the setting pokerconf.yml (folder path must be adjusted) --> you must be in the folder!
Furthermore, all other possible algorithms can be added by adding the appropriate path to the configuration file.

After this, start the local server with the config file. 
```
pypokergui serve poker_conf.yml --port 8000 --speed moderate
```

Then the browser will be opened and you will see registration page.

Please register yourself on the page (for example with your name) and start the game.

More information at: : https://github.com/ishikota/PyPokerGUI

Have fun playing poker!


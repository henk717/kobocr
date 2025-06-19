# kobocr
Listens to a scanners output folder and automatically processes it with AI, for use with KoboldCpp

# How to use
When you launch the script without a valid config file the default configuration files are automatically created.
This script makes use of the KoboldCpp API and is only compatible with KoboldCpp which can be obtained at https://koboldai.org/cpp

In the config.cfg you have the option to change the path of the input folder, either point your (network) scanner to the automatically generated input folder or edit the config to point to the location of the scanners output folder.

prompt.txt lets you define which instruction the AI should follow, this is already in the correct format for your AI (based on the chat adapter in KoboldCpp).
AI results will appear in the output folder.

# AGPL clarification
The infection of the AGPL license is a grey area, the intent is that if code from this script is used in your pipeline the user has a right to the a copy of this projects code including your modifications.
You do not have to make the programs open source that are part of your pipeline such as the scanner software or software that ingests the output folder.

# StrainDetect - a web server that detects viral strains from raw sequencing data accurately and efficiently
StrainDetect is an online viral strain-level analysis tool based on VirStrain. The back end of StrainDetect is implemented using Flask, and the front end is implemented using Vue.js. There are two components in StrainDetect. The first component is a GUI tool called StrainKmer, which allows the user to extract features from raw sequencing data on a personal PC. After acquiring the feature files, the user can upload the files to the second component, the Detect page of StrainDetect, to perform viral strain detection. The overall worflow of StrainDetect is shown below. 

<img width="500" height="400" src="https://user-images.githubusercontent.com/22760266/208287028-ab94e92c-7c5f-45f6-9a65-054d4a4fe935.png" alt="straindetect">

This reponstory includes the source code of StrainDetect. In addition, you can run StrainDetect locally by following the manual below.

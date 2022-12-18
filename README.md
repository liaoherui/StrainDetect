# StrainDetect - a web server that detects viral strains from raw sequencing data accurately and efficiently
[StrainDetect](https://strain.ee.cityu.edu.hk/) is an online viral strain-level analysis tool based on [VirStrain](https://github.com/liaoherui/VirStrain). The back end of StrainDetect is implemented using Flask, and the front end is implemented using Vue.js. There are two components in StrainDetect. The first component is a GUI tool called [StrainKmer](https://github.com/liaoherui/StrainKmer), which allows the user to extract features from raw sequencing data on a personal PC. After acquiring the feature files, the user can upload the files to the second component, the Detect page of StrainDetect, to perform viral strain detection. The overall worflow of StrainDetect is shown below. 

![home-page](https://user-images.githubusercontent.com/22760266/208290365-a75f3e57-cc8f-4610-8205-b3e5b54421e6.png)

This reponstory includes the source code of StrainDetect. In addition, you can run StrainDetect locally by following the manual below.

---------------------------------------------------------------------------
### Dependencies:
* Python ==3.6.* (3.6.12 is recommanded)
* node.js==v12.14.1
* npm==8.9.3

## Install

Build enviroment using the commands below:<BR/>
####
`git clone https://github.com/liaoherui/StrainDetect.git`<BR/>
`cd StrainDetect`<BR/>

Install Flask environment via [Anaconda](https://anaconda.org/):<BR/>
`conda env create -f environment.yaml`<BR/>

Install Vue.js environment via [npm](https://www.npmjs.com/):<BR/>
`cd front-end`<BR/>
`npm install`

## Run StrainDetect locally
####
Start Flask service using the commands below:<BR/>
`cd back-end`<BR/>
`flask run`

Start Vue.js service using the commands below:<BR/>
`cd front-end`<BR/>
`npm run dev`

Then, you can access StrainDetect via http://localhost:8080 locally.








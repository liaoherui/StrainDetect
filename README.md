# StrainDetect - a web server that detects viral strains from raw sequencing data accurately and efficiently
[StrainDetect](https://strain.ee.cityu.edu.hk/) is an online viral strain-level analysis tool based on [VirStrain](https://github.com/liaoherui/VirStrain). The back end of StrainDetect is implemented using Flask, and the front end is implemented using Vue.js. There are two components in StrainDetect. The first component is a GUI tool called [StrainKmer](https://github.com/liaoherui/StrainKmer), which allows the user to extract features from raw sequencing data on a personal PC. After acquiring the feature files, the user can upload the files to the second component, the Detect page of StrainDetect, to perform viral strain detection. The overall worflow of StrainDetect is shown below. 

![home-page](https://user-images.githubusercontent.com/22760266/208290365-a75f3e57-cc8f-4610-8205-b3e5b54421e6.png)

This reponstory includes the source code of StrainDetect. In addition, you can run StrainDetect locally by following the manual below.

import enchant
import pandas as pd
import numpy as np


csvwords = pd.read_csv(r"C:\Users\USER\Desktop\FAS\REFE\venv\afinn.csv")
matrix1 = csvwords[csvwords.columns[0]].to_numpy()
wordbank = np.array(matrix1.tolist())
matrix2 = csvwords[csvwords.columns[1]].to_numpy()
senscore = np.array(matrix2.tolist())


sen1 = input("Enter a Word: ")
sensplit = np.array(sen1.split())
threshold = 80.0
sentiscore = 0
print(sensplit)


for string1 in sensplit:
    counter = 0
    for string2 in wordbank:


        #Levenshtein
        lev = (enchant.utils.levenshtein(string1, string2))
        lev_score = (1 - (lev / max(len(string1), len(string2)))) * 100
        counter += 1

        #Sorrendice
        def dicematch(string1, string2):
            if not string1 or not string2:
                return 0

            if string1 == string2:
                return 1

            if (len(string1) < 2 or len(string2) < 2):
                return 0

            length1 = len(string1) - 1
            length2 = len(string2) - 1

            matches = 0
            i = 0
            j = 0

            while i < length1 and j < length2:
                a = string1[i:i + 2].lower()
                b = string2[j:j + 2].lower()

                if (a == b):
                    matches += 2

                i += 1
                j += 1

            return (matches / (length1 + length2))

        #Formula
        SD_score = (dicematch(string1, string2)*100)
        lev_score_low = (100 - lev_score) / (100 - threshold)
        lev_score_high = (lev_score - threshold) / (100 - threshold)
        SD_score_low = (100 - SD_score) / (100 - threshold)
        SD_score_high = (SD_score - threshold) / (100 - threshold)

        #Conditions
        if lev_score_high >= SD_score_high:
            MF_high = lev_score_high

        else:
            MF_high = SD_score_high

        if SD_score == 0:
            continue

        z1 = (lev_score +(MF_high*(100-threshold)))
        z2 = (SD_score +(MF_high*(100-threshold)))
        zn = ((lev_score * z1) + (SD_score * z2)) / (lev_score + SD_score)

        if zn >= threshold:
            print('The Tsukamoto Score of ' + string1 + ' and ' + string2 +' is :' + str(zn) + ' and comparable with each other')
            sentiscore = sentiscore + senscore[counter-1]


#Result
if sentiscore == 0:
    print("sentimental score : " + str(sentiscore) + " RESULT: NEUTRAL")

if sentiscore > 0:
    print("sentimental score : " + str(sentiscore) + " RESULT: POSITIVE")

if sentiscore < 0:
    print("sentimental score : " + str(sentiscore) + " RESULT: NEGATIVE")











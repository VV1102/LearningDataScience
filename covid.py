import csv
import re
from collections import defaultdict, Counter

def main():
    #data reading step
    with open('covidTrain.csv', 'r', encoding = 'utf-8') as f:
        reader = csv.DictReader(f)
        covidData = list(reader)

    #task 1 replacing age ranges with range average value
    for row in covidData:
        if row['age'] != 'NaN' and '-' in row['age']:
            match = re.search(r'(\d+)-(\d+)', row['age'])
            if match:
                start, end = int(match.group(1)), int(match.group(2))
                avgAge = round((start+end)/2)
                row['age'] = str(avgAge)


    #task 2 changing data format from dd.mm.yyyy to mm.dd.yyyy leave year part as is just
    #swap day and month parts for the three columns: date_onset_symptoms, date_admission_hospital
    # and date_confirmation
    dateColumns = ['date_onset_symptoms','date_admission_hospital','date_confirmation']
    for row in covidData:
        for col in dateColumns:
            if row[col] != 'NaN':
                parts = row[col].split('.')
                if len(parts) == 3:
                    day,month, year = parts  #simple way to keep track of all parts and store in vars
                    row[col] = f"{month}.{day}.{year}"  


    #task 3 filling in missing NaN values in latitude and longitude columns based on avg latitude
    #and longitude of that NaN value's province
    provinceLats = defaultdict(list)
    provinceLongs = defaultdict(list)

    for row in covidData:
        province = row['province']
        if row['latitude'] != 'NaN':
            provinceLats[province].append(float(row['latitude']))
        if row['longitude'] != 'NaN':
            provinceLongs[province].append(float(row['longitude']))

    #avg calcs
    provAvgLat = {p: round(sum(lats)/len(lats) , 2) if lats else 'NaN' for p, lats in provinceLats.items()}
    provAvgLong = {p: round(sum(longs)/len(longs) , 2) if longs else 'NaN' for p, longs in provinceLongs.items()}


    #now we fill in NaNs in latitude and longitude columns now that we have their designated values stored in our province to latitude and province to longitude dictionaries
    for row in covidData:
        province = row['province']
        if row['latitude'] == 'NaN' and province in provAvgLat:
            row['latitude'] = str(provAvgLat[province])
        if row['longitude'] == 'NaN' and province in provAvgLong:
            row['longitude'] = str(provAvgLong[province])

    #task 4 filling missing city column values based on the most common city value in that missing city column's rows province.  We check that province and look for the most occurring city corresponding to that province
    provinceCities = defaultdict(list)
    for row in covidData:
        province = row['province']
        city = row['city']
        if city != 'NaN':
            provinceCities[province].append(city)

    provinceCommonCity = {}
    for province, cities in provinceCities.items():
        cityCounts = Counter(cities)
        mostCommon = sorted(cityCounts.items(), key = lambda x: (-x[1],x[0]))  # this accounts for the tie and uses alphabetical order to select the right city to fill in NaN later
        if mostCommon:
            provinceCommonCity[province] = mostCommon[0][0]
    #fill in NaNs
    for row in covidData:
        province = row['province']
        if row['city'] == 'NaN' and province in provinceCommonCity:
            row['city'] = provinceCommonCity[province]


    #task 5 similar to last task we now have to fill in the missing(NaN) symptom values based on the most frequent symptom in the province of where the NaN value is from.  similar to last task use the same lambda function for the alphabetical order sorting list incase of a tie
    provinceSymptoms = defaultdict(list)
    for row in covidData:
        province = row['province']
        symptoms = row['symptoms']
        #fill in province to symptoms dictionary for values that aren't missing
        if symptoms != 'NaN':
            if '; ' in symptoms:
                symptomList = symptoms.split('; ')
            else:
                symptomList = symptoms.split(';')
            for symptom in symptomList:
                if symptom.strip():
                    provinceSymptoms[province].append(symptom.strip())

    #now we find the most common symptom per province by putting provinces in a dictionary and mapping them to their symptoms which is another dictionary of symptom counts
    provinceCommonSymptom = {}
    for province, symptoms in provinceSymptoms.items():
        symptomCounts = Counter(symptoms)
        mostCommon = sorted(symptomCounts.items(), key=lambda x:(-x[1],x[0]))
        if mostCommon:
            provinceCommonSymptom[province] = mostCommon[0][0]

    #now we can fill in the missing symptom values
    for row in covidData:
        province = row['province']
        if row['symptoms'] == 'NaN' and province in provinceCommonSymptom:
            row['symptoms'] = provinceCommonSymptom[province]


    #all tasks are complete now we write all of our outputs to a new csv file
    fieldNames = list(covidData[0].keys())
    with open('covidResult.csv', 'w', newline = '', encoding = 'utf-8') as f:
        writer = csv.DictWriter(f,fieldnames=fieldNames)
        writer.writeheader()
        writer.writerows(covidData)

main()
import csv

def main():
    # read from csv file
    data = []
    with open('pokemonTrain.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    
   
    calculateFirePokemonPercentage(data) 
    data = fillMissingTypes(data)
    data = fillMissingStats(data)
    writeToCsv(data, 'pokemonResult.csv')
    createTypePersonalityMapping(data)
    calculateStage3AverageHp(data)

def calculateFirePokemonPercentage(data):
    firePokemonCount = 0
    highLevelFirePokemonCount = 0
    
    for row in data:
        if row['type'] == 'fire':
            firePokemonCount += 1
            if float(row['level']) >= 40:
                highLevelFirePokemonCount += 1
    
    # percentage calculation
    if firePokemonCount > 0:
        perc = (highLevelFirePokemonCount / firePokemonCount) * 100
        perc = round(perc)  
    else:
        perc = 0
    
    #writing to output file
    with open('pokemon1.txt', 'w') as output_file:
        output_file.write(f"Percentage of fire type Pokemons at or above level 40 = {perc}")
    
    return perc

def fillMissingTypes(data):
    #dict to count howmany types for each weakness
    weaknessToTypes = {}
    
    for row in data:
        if row['type'] != 'NaN' and row['weakness'] != 'NaN':
            weakness = row['weakness']
            pokemonType = row['type']
            
            if weakness not in weaknessToTypes:
                weaknessToTypes[weakness] = {}
            
            if pokemonType not in weaknessToTypes[weakness]:
                weaknessToTypes[weakness][pokemonType] = 0
            
            weaknessToTypes[weakness][pokemonType] += 1
    
    mostCommonType = {}
    for weakness, types in weaknessToTypes.items():
        maxCount = max(types.values())
        mostCommon = [t for t, count in types.items() if count == maxCount]
        #sort to make finding highest common type easier
        mostCommon.sort()
        mostCommonType[weakness] = mostCommon[0]
    
    #main part of method to fill in missing NaNs of type column from all the dictionaries we made
    for row in data:
        if row['type'] == 'NaN' and row['weakness'] in mostCommonType:
            row['type'] = mostCommonType[row['weakness']]
    
    return data

def fillMissingStats(data):
    # Separate Pokemon by level threshold (40)
    highLevel = []
    lowLevel = []
    
    for row in data:
        if float(row['level']) > 40:
            highLevel.append(row)
        else:
            lowLevel.append(row)
    
    #avg calculations for high lvl Pokemon
    highAtkSum = 0
    highAtkCount = 0  
    highDefSum = 0   
    highDefCount = 0 
    highHpSum = 0 
    highHpCount = 0  
    
    for row in highLevel:
        if row['atk'] != 'NaN':
            highAtkSum += float(row['atk'])
            highAtkCount += 1
        if row['def'] != 'NaN':
            highDefSum += float(row['def'])
            highDefCount += 1
        if row['hp'] != 'NaN':
            highHpSum += float(row['hp'])
            highHpCount += 1
    
    highAtkAvg = round(highAtkSum / highAtkCount, 1) if highAtkCount > 0 else 0
    highDefAvg = round(highDefSum / highDefCount, 1) if highDefCount > 0 else 0
    highHpAvg = round(highHpSum / highHpCount, 1) if highHpCount > 0 else 0
    
    # avg calculations for low lvl Pokemon
    lowAtkSum = 0 
    lowAtkCount = 0  
    lowDefSum = 0
    lowDefCount = 0   
    lowHpSum = 0   
    lowHpCount = 0
    
    for row in lowLevel:
        if row['atk'] != 'NaN':
            lowAtkSum += float(row['atk'])
            lowAtkCount += 1
        if row['def'] != 'NaN':
            lowDefSum += float(row['def'])
            lowDefCount += 1
        if row['hp'] != 'NaN':
            lowHpSum += float(row['hp'])
            lowHpCount += 1
    
    lowAtkAvg = round(lowAtkSum / lowAtkCount, 1) if lowAtkCount > 0 else 0
    lowDefAvg = round(lowDefSum / lowDefCount, 1) if lowDefCount > 0 else 0
    lowHpAvg = round(lowHpSum / lowHpCount, 1) if lowHpCount > 0 else 0
    
    # fill in NaNs
    for row in data:
        if float(row['level']) > 40:
            if row['atk'] == 'NaN':
                row['atk'] = str(highAtkAvg)
            if row['def'] == 'NaN':
                row['def'] = str(highDefAvg)
            if row['hp'] == 'NaN':
                row['hp'] = str(highHpAvg)
        else:
            if row['atk'] == 'NaN':
                row['atk'] = str(lowAtkAvg)
            if row['def'] == 'NaN':
                row['def'] = str(lowDefAvg)
            if row['hp'] == 'NaN':
                row['hp'] = str(lowHpAvg)
    
    return data

def writeToCsv(data, filename):
    # get the fieldnames from the first row
    fieldnames = list(data[0].keys())
    
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def createTypePersonalityMapping(data):
    # make dictionary for type to personality
    typeToPersonality = {}
    
    for row in data:
        pokemonType = row['type']
        personality = row['personality']
        
        if pokemonType not in typeToPersonality:
            typeToPersonality[pokemonType] = []
        
        if personality not in typeToPersonality[pokemonType]:
            typeToPersonality[pokemonType].append(personality)
    
    #sort types in type to personalities in ascending order
    for pokemonType in typeToPersonality:
        typeToPersonality[pokemonType].sort()
    
    with open('pokemon4.txt', 'w') as output_file:
        output_file.write("Pokemon type to personality mapping:\n\n")
        
        for pokemonType in sorted(typeToPersonality.keys()):
            personalities = ", ".join(typeToPersonality[pokemonType])
            output_file.write(f"   {pokemonType}: {personalities}\n")
    
    return typeToPersonality

def calculateStage3AverageHp(data):  
    stage3HpSum = 0
    stage3Count = 0
    
    for row in data:
        if row['stage'] == '3.0' and row['hp'] != 'NaN':
            stage3HpSum += float(row['hp'])
            stage3Count += 1
    
    if stage3Count > 0:
        averageHp = round(stage3HpSum / stage3Count)
    else:
        averageHp = 0
    
    with open('pokemon5.txt', 'w') as output_file:
        output_file.write(f"Average hit point for Pokemons of stage 3.0 = {averageHp}")
    
    return averageHp


main()
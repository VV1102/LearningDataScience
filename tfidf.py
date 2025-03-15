import re
import math
from collections import defaultdict, Counter

"""
    steps to clean text
    1. remove website links
    2. remove non-word characters
    3. normalize whitespace 
    4. convert to lowercase 
"""

def readFile(filePath):
    with open(filePath, 'r', encoding='utf-8') as file:
        return file.read()

def writeFile(filePath, content):
    with open(filePath, 'w', encoding='utf-8') as file:
        file.write(content)

def cleanText(text):
    text = re.sub(r'https?://\S+', '', text)  # remove urls
    text = re.sub(r'[^a-zA-Z0-9_\s]', '', text)  # keep letters, digits, underscores, spaces
    text = re.sub(r'\s+', ' ', text).strip()  # normalize spaces
    return text.lower()  # convert to lowercase

def removeStopwords(text, stopwords):
    words = text.split()
    return ' '.join(word for word in words if word not in stopwords)

def stemWords(text):
    words = text.split()
    stemmed = []
    for word in words:
        if word.endswith('ing'):
            stemmed.append(word[:-3])
        elif word.endswith('ly'):
            stemmed.append(word[:-2])
        elif word.endswith('ment'):
            stemmed.append(word[:-4])
        else:
            stemmed.append(word)
    return ' '.join(stemmed)

def preprocessDocument(docText, stopwords): 
    cleaned = cleanText(docText)
    noStopwords = removeStopwords(cleaned, stopwords) 
    stemmed = stemWords(noStopwords)
    return stemmed

def computeTf(docText):
    words = docText.split()
    if not words:
        return {}
    wordCount = Counter(words) 
    totalWords = len(words)
    return {word: count / totalWords for word, count in wordCount.items()}

def computeIdf(docs): 
    totalDocs = len(docs) 
    wordInDocs = defaultdict(int)
    for doc in docs:
        uniqueWords = set(doc.split())
        for word in uniqueWords:
            wordInDocs[word] += 1
    return {word: math.log(totalDocs / count) + 1 for word, count in wordInDocs.items()}

def computeTfidf(tf, idf):
    return {word: round(tf[word] * idf.get(word, 0), 2) for word in tf}

def getTop5Words(tfidf):
    return sorted(tfidf.items(), key=lambda x: (-x[1], x[0]))[:5]

def main():
    #step 1: read the list of documents from tfidf_docs.txt
    docFiles = readFile('tfidf_docs.txt').splitlines() 
    
   # step 2: load the stopwords
    stopwords = set(readFile('stopwords.txt').splitlines())
    
    # step 3: preprocess each document and save results 
    preprocessedDocs = {}
    for docFile in docFiles:
        docFile = docFile.strip()  # Ensure no extra spaces or newlines 
        docText = readFile(docFile)
        preprocessedText = preprocessDocument(docText, stopwords)
        preprocessedDocs[docFile] = preprocessedText
        writeFile(f'preproc_{docFile}', preprocessedText)  # Write preprocessed text
    
      # step 4: calculate TF-IDF scores for all documents
    idf = computeIdf(preprocessedDocs.values())
    
    # step 5: find top 5 words for each document and save results
    for docFile, preprocessedText in preprocessedDocs.items():
        tf = computeTf(preprocessedText)
        tfidf = computeTfidf(tf, idf)
        top_5 = getTop5Words(tfidf)
        # format the output as a list of tuples in 1 line
        output = '[' + ', '.join(f"('{word}', {score:.2f})" for word, score in top_5) + ']'
        writeFile(f'tfidf_{docFile}', output)


main()
import sys
import requests
import re
import json

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from bs4 import BeautifulSoup

# Load the model and tokenizer
model_name = "facebook/bart-large-mnli"
#tokenizer = AutoTokenizer.from_pretrained(model_name)
#model = AutoModelForCausalLM.from_pretrained(model_name)

# Initialize the pipeline
#classifier = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer)
classifier = pipeline("zero-shot-classification", model=model_name)

# Define categories
categories = ["engineering", "research", "entertainment", "gaming", "communication", "shopping", "other"]

domain_keywords = {
    'research': [
        'canvas',
        'edu',
        'university',
        'college',
        'school',
        'learn',
        'classroom',
        'student',
        'teacher',
        'homework',
        'assignment',
        'grade',
        'exam',
        'quiz',
        'lecture',
        'syllabus',
        'study',
        'research',
        'academy',
        'library',
        'textbook',
        'professor',
        'academic',
        'scholar',
        'tuition',
        'campus',
        'dormitory',
        'graduation',
        'diploma',
        'degree',
        'alumni',
        'scholarship',
        'tuition',
        'enroll',
        'admission',
        'application',
        'major',
        'minor',
        'masters',
        'bachelors',
        'doctorates',
        'phd',
        'postdoc',
        'thesis',
        'dissertation',
        'research',
        'publication',
        'conference',
        'seminar',
        'workshop',
        'lab',
        'experiment',
        'gatech',
        'georgia tech',
        'gatech.edu',
        'gatech.instructure',
        'math',
        'science',
        'engineering',
        'technology',
        'computer science',
        'physics',
        'chemistry',
        'biology',
        'geology',
        'astronomy',
        'psychology',
        'sociology',
        'economics',
        'history',
        'philosophy',
        'literature',
        'language',
        'linguistics',
        'art',
        'internship',
        'intern',
        'co-op',
        'research',
        'job',
        'career',
        'employment',
        'recruitment',
        'hire',
        'resume',
        'cv',
        'cover letter',
        'interview',
        'network',
        'linkedin',
        'career fair',
        'job fair',
        'recruiter',
        'employer',
        'employee',
        'pearson',
        'mcgraw-hill',
        'cengage',
        'qualtrics',
        'course',
        'class',
        'lesson',
        'lecture',
        'coursehero',
        'quizlet',
        'khan academy',
        'coursera',
        'edx',
        'udemy',
        'udacity',
        'chegg',
        'd2l',
        'blackboard',
        'moodle',
        'canvas',
        'brightspace',
        'edmodo',
        'google classroom',
        'docs',
        'slides',
        'sheets',
        'forms',
        'drive',
        'calendar',
        'meet',
        'google',
        'microsoft',
        'office',
        'word',
        'powerpoint',
        'excel',
        'outlook',
        'teams',
        'zoom',
        'slack',
        'docs.google',
    ], 
    'engineering': [
        'https://idx.google.com/',
        'github',
        'gitlab',
        'dev',
        'developer',
        'stackoverflow',
        'debug',
        'codecademy',
        'w3schools',
        'freecodecamp',
        'hackerrank',
        'leetcode',
        'codeforces',
        'topcoder',
        'codewars',
        'projecteuler',
        'geeksforgeeks',
        'rosalind',
        'codepen',
        'bitbucket',
        'python',
        'java',
        'javascript',
        'typescript',
        'html',
        'css',
        'sass',
        'less',
        'php',
        'ruby',
        'perl',
        'c++',
        'c#',
        #'c',
        'objective-c',
        'swift',
        'kotlin',
        'scala',
        #'r',
        'rust',
        'go',
        'dart',
        'lua',
        'shell',
        'bash',
        'powershell',
        'batch',
        'awk',
        'sed',
        'regex',
        'code',
        'coding',
        'program',
        'programming',
        'developer',
        'development',
        'software',
        'engineer',
        'engineering',
        'computer',
        'computing',
        'algorithm',
        'data structure',
        'frontend',
        'backend',
        'fullstack',
        'database',
        'data',
        'web',
        'app',
        'application',
        'site',
        'website',
        'server',
        'client',
        'database',
        'sql',
        'nosql',
        'mongodb',
        'mysql',
        'postgresql',
        'sqlite',
        'oracle',
        'microsoft sql server',
        'microsoft access',
        'microsoft azure',
        'amazon rds',
        'amazon dynamodb',
        'amazon aurora',
        'amazon redshift',
        'google cloud',
        'gcp',
        'firebase',
        'bigquery',
        'bigtable',
        'aws',
        'azure',
        'cloud',
        'serverless',
        'microservices',
        'container',
        'saas',
        'paas',
        'iaas',
        'api',
        'rest',
        'graphql',
        'soap',
        'web service',
        'cloud computing',
        'virtualization',
        'containerization',
        'kubernetes',
        'docker',
        'helm',
        'hardware',
        'electronics',
        'circuit',
        'microcontroller',
        'arduino',
        'raspberry pi',
        'robotics',
        'automation',
        'control',
        'signal',
        'communication',
        'network',
        'internet',
        'protocol',
        'model',
        'architecture',
        'design',
        'pattern',
        'paradigm',
        'methodology',
        'framework',
        'library',
        'tool',
        'ide',
        'editor',
        'debugger',
        'compiler',
        'interpreter',
        'runtime',
        'environment',
        'os',
        'operating system',
        'neural network',
        'deep learning',
        'machine learning',
        'artificial intelligence',
        'data science',
        'big data',
        'analytics',
        'visualization',
        'statistics',
        'mathematics',
        'physics',
        'matlab',
        'processing',
        'programming language',
        'generation',
        'compilation',
        'interpretation',
        'execution',
        'testing',
        'debugging',
        'optimization',
        'refactoring',
        'documentation',
        'version control',
        'git',
        'svn',
        'mercurial',
        'perforce',
        'excel',
        'calc',
        'computer aided design',
        'cad',
        'computer',
        'electrical',
        'mechanical',
        'civil',
        'chemical',
        'aerospace',
        'biomedical',
        'environmental',
        'industrial',
        'systems',
        'control',
        'automotive',
        'robotics',
        'manufacturing',
        'production',
        'process',
        'material',
        'energy',
    ],
    'communication': [
        'facebook',
        'twitter',
        'instagram',
        'linkedin',
        'snapchat',
        'tiktok',
        'whatsapp',
        'messenger',
        'wechat',
        'telegram',
        'discord',
        'reddit',
        'pinterest',
        'tumblr',
        'flickr',
    ],
    'shopping': [
        'amazon',
        'ebay',
        'etsy',
        'shopify',
        'walmart',
        'target',
        'best buy',
        'costco',
        'alibaba',
        'aliexpress',
        'dhgate',
    ],
    'entertainment': [
        'youtube',
        'news',
        'netflix',
        'hulu',
        'disney',
        'prime video',
        'apple tv',
        'hbo',
        'max',
        'cbs',
        'magazine',
        'newspaper',
        'nbc',
        'abc',
        'fox news',
        'fox sports',
        'cnn',
        'msnbc',
        'espn',
        'nfl',
        'nba',
        'mlb',
        'nhl',
        'ufc',
        'mma',
        'wwe',
        'aew',
        'nascar',
        'indycar',
        'f1',
    ],
    'gaming': [
        'steam',
        'epic games',
        'origin',
        'uplay',
        'battle.net',
        'playstation',
        'xbox',
        'nintendo',
        'switch',
        'game',
        'gaming',
        'videogame',
        'console',
        'pc',
    ]
}

def fetch_page_content(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL content: {e}")
        return ""

def extract_text_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def categorize_by_domain(url):
    keyword_counts = {category: 0 for category in categories}
    for category, keywords in domain_keywords.items():
        for keyword in keywords:
            if keyword in str(url).lower():
                #return category
                keyword_counts[category] += 1
    #return "other"
    # Sort the categories by the number of keywords found in the URL
    sorted_categories = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_categories

def categorize_url(url):
    domain_category = categorize_by_domain(url)
    model_category = classifier(url, categories)

    if domain_category[0][1] == 0 and model_category["scores"][0] < 0.4:
        page_content = fetch_page_content(url)
        text_content = extract_text_from_html(page_content)
        model_category = classifier(text_content, categories)
        domain_category = categorize_by_domain(text_content)

    print("Domain Category Counts:", json.dumps(domain_category, indent=2))
    print("Model Category:", json.dumps(model_category, indent=2))

    if domain_category[0][0] == model_category["labels"][0] and model_category["scores"][0] > 0.4 and domain_category[0][1] > 0:
        return model_category["labels"][0]
    if model_category["scores"][0] >= 0.4 and model_category["labels"][0] != "other":
        return model_category["labels"][0]
    if model_category["scores"][0] < 0.4 and domain_category[0][1] > 0:
        return domain_category[0][0]
    if model_category["labels"][0] == "other" and domain_category[0][1] > 0:
        return domain_category[0][0]
    if domain_category[0][1] == 0 and model_category["labels"][0] != "other":
        return model_category["labels"][0]
    return "other"

if __name__ == "__main__":
    url = sys.argv[1]
    print(categorize_url(url))
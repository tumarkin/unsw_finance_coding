import requests
import gzip

def get_index():
    url = 'https://www.sec.gov/Archives/edgar/full-index/2022/QTR1/master.gz'
    headers = { 'user-agent': 'r.tumarkin@unsw.edu.au'}
    response = requests.get(url, headers=headers)
    binary_index = gzip.decompress(response.content)
    index = binary_index.decode('ascii')
    
    with open('index/2022.Q1.master.txt', 'w') as out:
        out.write(index)
    

if __name__ == '__main__':
    get_index()

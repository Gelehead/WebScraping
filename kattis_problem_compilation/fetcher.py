from bs4 import BeautifulSoup as bs
import requests
import json

def all_problems():
    problems = []
    page_number = int(bs(requests.get(f"https://open.kattis.com/problems?page=1").content, 'html.parser').findAll('a', class_='button')[-1].text)
    problem_count = 0
    for page in range(1, page_number):
        soup = bs(requests.get(f"https://open.kattis.com/problems?page={page}").content, 'html.parser')
        table = soup.findAll('table', class_="table2")[1]
        for row in table.find('tbody').findAll('tr'):
            data = row.findAll('td')
            
            problem_link = "https://open.kattis.com"+ data[0].find('a')['href']
            stats_link = ("https://open.kattis.com" + data[7].find('a')['href'])[:-2] + 'statistics'

            problem_soup = bs(requests.get(problem_link).content, 'html.parser')
            stats_soup = bs(requests.get(stats_link).content, 'html.parser')

            source_link = bs(requests.get(problem_link + '?tab=metadata').content, 'html.parser').find('div', class_='card my-0 metadata-license-card')
            author_exists = source_link.find('span', class_='flex flex-wrap gap-3')
            info = author_exists.find_next_sibling().find('a') if author_exists != None else source_link.find('a')
            prob_source = {
                'source name': info.text,
                'source link': info['href']
            }

            num_examples = len(problem_soup.findAll('table'))
            prb_lgth = len(''.join([x.text for x in problem_soup.find('div', class_='problembody').findAll('p')]))


            # Gather statistics
            statistics = {
                'submissions': int(data[3].text.replace(',', '')),
                'accepted_submissions': int(data[4].text.replace(',', '')),
                'submission_ratio': float(data[5].text.strip('%')) / 100,
                'fastest_solution': data[1].text,
                'shortest_solution': data[2].text
            }

            # Append problem data
            problems.append({
                'problem_name': data[0].text,
                'languages': [lang.text for lang in data[7].find_all('span')],
                'description_length': prb_lgth,
                'number_of_examples': num_examples,
                'difficulty': float(data[6].text[:3]),
                'statistics': statistics,
                'problem_source': prob_source
            })

            problem_count += 1
            print(f"Processed problem {problem_count} : {data[0].text}")

    return problems
    
problems = all_problems()
with open('all_problems_kattis.json', 'w', encoding='utf-8') as f:
    json.dump(problems, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    with multiprocessing.Pool()
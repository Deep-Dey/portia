from typing import List
import requests
from bs4 import BeautifulSoup
from portia_types.pubmed_article import ArticleDictionary
from web_scrapper.pubmed_data_fetcher import PubmedDataFetcher


class PubMedScrapper:

    _pdf: PubmedDataFetcher

    def __init__(self):
        self._pdf = PubmedDataFetcher()

    @classmethod
    def fetch_article_details(cls, tag: str) -> ArticleDictionary:

        article_link: str = "https://pubmed.ncbi.nlm.nih.gov" + tag
        html_content = requests.get(article_link).text
        soup = BeautifulSoup(html_content, "lxml")

        article_details: ArticleDictionary = {
            'link': article_link,
            'title': cls._pdf.fetch_article_title(soup),
            'author': cls._pdf.fetch_article_author(soup),
            'pm_id': cls._pdf.fetch_article_pm_id(soup),
            'pmc_id': cls._pdf.fetch_article_pmc_id(soup),
            'doi': cls._pdf.fetch_article_doi_id(soup),
            'abstract': cls._pdf.fetch_article_abstract(soup),
            'citation': None
        }

        return article_details

    @classmethod
    def fetch_article_details_list(cls, tag_list: List[str], get_citation: bool = False) -> List[ArticleDictionary]:

        article_detail_list: List[ArticleDictionary] = []

        for tag in tag_list:
            article_detail_list.append(cls.fetch_article_details(tag))

        if get_citation:

            # TODO: is this a good way?
            from web_automator import pubmed_citation_automator as pca
            citation = pca.get_article_citation(tag_list)

            for i in range(len(article_detail_list)):
                article_detail_list[i]['citation'] = citation[i]

        return article_detail_list

    @classmethod
    def get_associate_search_result(cls, tag, get_citation=False) -> List[ArticleDictionary]:

        generated_tag_list: List[str] = []
        url = "https://pubmed.ncbi.nlm.nih.gov/?term=" + tag.replace(' ', '+')
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, "lxml")

        if 'No results were found.' in str(soup.find("div", attrs={"class": "results-amount"}).text):
            print("Your Keyword is wrong")
            exit()
        else:
            article_content = soup.find_all("article", attrs={"class": "full-docsum"})
            for article in article_content:
                generated_tag_list.append(str(article.find("a", attrs={"class": "docsum-title"})['href']).strip())

        return cls.fetch_article_details_list(generated_tag_list, get_citation)

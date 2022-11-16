import scrapy


class NcaafSpider(scrapy.Spider):
    name = 'ncaaf'
    # allowed_domains = ['https://www.sports-reference.com']
    start_urls = ['https://www.sports-reference.com/cfb/years//']

    def parse(self, response):
        for year_link in response.xpath('//table[@id="years"]/tbody/tr/th/a'):
            url = year_link.xpath('@href').get()
            yield scrapy.Request(response.urljoin(url), self.parse_year)

    def parse_year(self, response):
        url = response.xpath('//div[@id="inner_nav"]//li[.="Schedule & Scores"]').xpath('a/@href').get()
        yield scrapy.Request(response.urljoin(url), self.parse_schedule)

    def parse_schedule(self, response):
        table = response.xpath('//table')
        for row  in table.xpath('tbody/tr'):
            week       = row.xpath('td[@data-stat="week_number"]/text()').get()
            date       = row.xpath('td[@data-stat="date_game"]/a/text()').get()
            winner     = row.xpath('td[@data-stat="winner_school_name"]/a/text()').get()
            winner_pts = row.xpath('td[@data-stat="winner_points"]/text()').get()
            loser      = row.xpath('td[@data-stat="loser_school_name"]/a/text()').get()
            loser_pts  = row.xpath('td[@data-stat="loser_points"]/text()').get()
            yield { 'week': week
                  , 'date': date
                  , 'winner': winner
                  , 'winner_pts': winner_pts
                  , 'loser': loser
                  , 'loser_pts': loser_pts
                  }

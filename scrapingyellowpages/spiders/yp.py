import scrapy


class YpSpider(scrapy.Spider):
    name = 'yp'
    start_urls = ['https://www.yellowpages.ca/search/si/1/interior+designer/Mississauga+ON']

    def parse(self, response):
        items = response.css('div.page__content.jsListingMerchantCards.jsListContainer')
        for item in items:
            yield {
                'business_name' : item.css('h3 > a ::text').get(),
                'phone_number' : item.css('li.mlr__item.mlr__item--more.mlr__item--phone.jsMapBubblePhone > a ::attr(data-phone)').get(default=''),
                'website' : response.urljoin(item.css('li.mlr__item.mlr__item--website > a ::attr(href)').get(default='')),
            }

        next_page = response.css('div.view_more_section_noScroll > a ::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
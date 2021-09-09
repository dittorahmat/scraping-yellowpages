import scrapy


class YpSpider(scrapy.Spider):
    name = 'yp'
    start_urls = ['https://www.yellowpages.ca/search/si/1/interior+designer/Mississauga+ON']

    def parse(self, response):
        items = response.css('div.listing__content__wrapper')
        for item in items:
            try:
                addr = item.css('span.listing__address--full ::text').extract()
                addr = ''.join(addr).replace('\n', '')
            except:
                addr = ''
            try:
                web = item.css('li.mlr__item.mlr__item--website > a ::attr(href)').get()
                if web is not None:
                    web = response.urljoin(web)
                else:
                    web=''
            except:
                web = ''
            yield {
                'business_name' : item.css('h3 > a ::text').get(),
                'address' : addr,
                'phone_number' : item.css('li.mlr__item.mlr__item--more.mlr__item--phone.jsMapBubblePhone > a ::attr(data-phone)').get(default=''),
                'website' : web,
            }

        next_page = response.css('div.view_more_section_noScroll > a ::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
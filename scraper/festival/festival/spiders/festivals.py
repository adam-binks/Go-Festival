# -*- coding: utf-8 -*-
import scrapy, logging


class FestivalsSpider(scrapy.Spider):
    name = "festivals"

    # just do UK festivals for now
    start_urls = ["https://www.musicfestivalwizard.com/festival-guide/uk-festivals/"]

    def parse(self, response):
        # returns the page number of this url
        def get_page_num(url):
            try:
                return int(response.url[-2])
            except ValueError:  # this url doesn't have /page/x/ on the end, so must be page 1
                return 1

        # returns a url with page current_num replaced by new_num
        def replace_page_num(url, current_num, new_num):
            new_url = url
            if not url.endswith("/page/" + str(current_num) + "/"):
                new_url += "/page/"
            else:
                new_url = new_url[:-2]  # take off the "/" and the page num preceding it
            return new_url + str(new_num) + "/"

        # returns true if number of festivals found > 0
        def festivals_were_found(response):
            festival_count_text = response.css(".festival-count ::text").extract_first().rstrip()
            festival_count_text = festival_count_text.replace('\r', '').replace('\n',
                                                                                '')  # get rid of newline characters

            logging.debug("\n\n\n\n\n\n\n\n\n\n" + festival_count_text)

            return "found 0 festivals" not in festival_count_text

        logging.debug("Festivals were found? " + str(festivals_were_found(response)))

        if not festivals_were_found(response):  # either no festivals exist or we've hit the last page of results
            return

        # follow links to festival pages and parse each one
        for href in response.css(".festivaltitle a::attr(href)"):
            yield response.follow(href, self.parse_festival)

        # follow pagination links, call this method recursively
        current_page_num = get_page_num(response.url)
        next_page_url = replace_page_num(response.url, current_page_num, current_page_num + 1)

        yield response.follow(next_page_url, self.parse)

    def parse_festival(self, response):

        def css_extract_first(query):
            return response.css(query).extract_first().strip()

        def css_extract_all(query):
            return response.css(query).extract()

        # store all of the details to return
        festival_details = {"NAME": css_extract_first(".breadcrumb_last::text")}

        # grab the big chunk of text as an array of strings
        raw_basic_details = css_extract_all("#festival-basics ::text")
        basic_details = {}

        # find the subheading, then grab the next line because that contains the data we want
        for detail in ["WHEN:", "WHERE:", "TICKETS:", "CAMPING:", "THE SCENE"]:
            try:
                index = raw_basic_details.index(detail)
                # store without the colon to be a bit nicer
                basic_details[detail.strip(":")] = raw_basic_details[index + 1].strip()
            except ValueError:
                # if a detail can't be found, just skip it, record a blank string
                basic_details[detail.strip(":")] = ""

        # add the basic_details to the rest of the details
        festival_details.update(basic_details)

        # extract the full lineup
        start_index = raw_basic_details.index("THE 2017 LINEUP") + 1
        lineup = []
        for i in range(start_index, len(raw_basic_details)):
            artist = raw_basic_details[i].strip().upper()
            if "\n" not in artist and "\r" not in artist and artist is not '' and artist not in lineup:
                lineup.append(artist)

        festival_details["LINEUP"] = lineup

        yield festival_details
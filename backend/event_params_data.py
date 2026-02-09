from models.event_params import EventParams
from models.track import Track
from webscraper.jms_site_params import JmsSiteParams
from webscraper.myraceresult_params import MyRaceResultParams

"""
All participants :
https://my4.raceresult.com/192607/RRPublish/data/list?key=9d484a9a9259ff0ae1a4a8570861bc3b&listname=Participants%7CParticipants%20List%20123&page=participants&contest=0&r=all&l=0


https://my4.raceresult.com/192607/RRPublish/data/list?key=9d484a9a9259ff0ae1a4a8570861bc3b&listname=Participants%7CParticipants%20List%20123&page=participants&contest=0&r=all&l=0

Lap details for a given athlete (pid=421 here) :
https://my4.raceresult.com/192607/RRPublish/data/list?key=9d484a9a9259ff0ae1a4a8570861bc3b&listname=Online%7CLap%20Details&page=live&contest=0&r=pid&pid=421


Miami 2013 https://jms.racetecresults.com/results.aspx?CId=16370&RId=13
Miami 2014 https://jms.racetecresults.com/results.aspx?CId=16370&RId=67
Miami 2015 https://jms.racetecresults.com/results.aspx?CId=16370&RId=121  # Age group available as 'category' column
Miami 2016 https://jms.racetecresults.com/results.aspx?CId=16370&RId=179
Miami 2017 https://jms.racetecresults.com/results.aspx?CId=16370&RId=240
Miami 2018 https://jms.racetecresults.com/results.aspx?CId=16370&RId=294
Miami 2019 https://jms.racetecresults.com/results.aspx?CId=16370&RId=352
Miami 2020 https://jms.racetecresults.com/results.aspx?CId=16370&RId=400
Miami 2021 https://jms.racetecresults.com/results.aspx?CId=16370&RId=413
Miami 2022 https://my.raceresult.com/192607
Miami 2023 https://my.raceresult.com/204047
Miami 2024 https://my.raceresult.com/259072
Miami 2025 https://my.raceresult.com/310199/
"""

MIAMI = ("Homestead Speedway", "Homestead", 1.46)
SPAARNDAM = ("Wheelerplanet", "Spaarndam", 2.0)

homestead_track = Track(
    name="Homestead Speedway", city="Homestead", country="USA", length_miles=1.46
)

miami_event_params: dict[int, EventParams] = {
    2013: EventParams(
        date="2013-01-07",
        track=homestead_track,
        scraped_site_params=JmsSiteParams(
            ranking_home_url="https://jms.racetecresults.com/results.aspx?CId=16370&RId=13",
            categories_indexes=[1],
            position_col_index=0,
            name_col_index=2,
        ),
    ),
    2014: EventParams(
        date="2014-01-20",
        track=homestead_track,
        scraped_site_params=JmsSiteParams(
            ranking_home_url="https://jms.racetecresults.com/results.aspx?CId=16370&RId=67",
            categories_indexes=[1, 2, 3, 4],
            position_col_index=0,
            name_col_index=2,
        ),
    ),
    2015: EventParams(
        date="2015-02-12",
        track=homestead_track,
        scraped_site_params=JmsSiteParams(
            ranking_home_url="https://jms.racetecresults.com/results.aspx?CId=16370&RId=121",
            categories_indexes=[1, 2, 3, 4],
            position_col_index=0,
            name_col_index=1,
        ),
    ),
    2016: EventParams(
        date="2016-02-26",
        track=homestead_track,
        scraped_site_params=JmsSiteParams(
            ranking_home_url="https://jms.racetecresults.com/results.aspx?CId=16370&RId=179",
            categories_indexes=[1, 2, 3, 4],
            position_col_index=1,
            name_col_index=2,
        ),
    ),
    2017: EventParams(
        date="2017-01-16",
        track=homestead_track,
        scraped_site_params=JmsSiteParams(
            ranking_home_url="https://jms.racetecresults.com/results.aspx?CId=16370&RId=240",
            categories_indexes=[1, 3, 4],
            position_col_index=1,
            name_col_index=3,
        ),
    ),
    2018: EventParams(
        date="2018-01-10",
        track=homestead_track,
        scraped_site_params=JmsSiteParams(
            ranking_home_url="https://jms.racetecresults.com/results.aspx?CId=16370&RId=294",
            categories_indexes=[1, 3, 4],
            position_col_index=1,
            name_col_index=3,
        ),
    ),
    2019: EventParams(
        date="2019-01-18",
        track=homestead_track,
        scraped_site_params=JmsSiteParams(
            ranking_home_url="https://jms.racetecresults.com/results.aspx?CId=16370&RId=352",
            categories_indexes=[1, 2, 3, 4],
            position_col_index=1,
            name_col_index=3,
        ),
    ),
    2020: EventParams(
        date="2020-01-17",
        track=homestead_track,
        scraped_site_params=JmsSiteParams(
            ranking_home_url="https://jms.racetecresults.com/results.aspx?CId=16370&RId=400",
            categories_indexes=[1, 2, 3, 4, 5],
            position_col_index=1,
            name_col_index=3,
        ),
    ),
    2021: EventParams(
        date="2021-01-29",
        track=homestead_track,
        scraped_site_params=JmsSiteParams(
            ranking_home_url="https://jms.racetecresults.com/results.aspx?CId=16370&RId=413",
            categories_indexes=[1, 3, 5],
            position_col_index=1,
            name_col_index=4,
            athlete_link_col_index=2,
        ),
    ),
    2022: EventParams(
        date="2022-02-19",
        track=homestead_track,
        scraped_site_params=MyRaceResultParams(
            race_id=192607,
            ranking_home_url="https://my4.raceresult.com/192607/RRPublish/data/list?key=9d484a9a9259ff0ae1a4a8570861bc3b&listname=Participants%7CParticipants%20List%20123&page=participants&contest=0&r=all&l=0",
            athlete_middle_url="/RRPublish/data/list?key=9d484a9a9259ff0ae1a4a8570861bc3b&listname=Online%7CLap%20Details&page=live&contest=0&r=pid&pid=",
            age_category_col_index=6,
            discipline_col_index=7,
            gender_col_index=8,
        ),
    ),
    2023: EventParams(
        date="2023-02-10",
        track=homestead_track,
        scraped_site_params=MyRaceResultParams(
            race_id=204047,
            ranking_home_url="https://my4.raceresult.com/204047/RRPublish/data/list?key=b02d8bcb6d81d09372a43de65f7f7d48&listname=Participants%7CIndividual%20Skaters&page=participants&contest=0&r=all&l=0",
            athlete_middle_url="/RRPublish/data/list?key=b02d8bcb6d81d09372a43de65f7f7d48&listname=Online%7CLap%20Details&page=live&contest=0&r=pid&pid=",
            age_category_col_index=5,
            discipline_col_index=6,
            gender_col_index=7,
        ),
    ),
    2024: EventParams(
        date="2024-02-15",
        track=homestead_track,
        scraped_site_params=MyRaceResultParams(
            race_id=259072,
            ranking_home_url="https://my1.raceresult.com/259072/RRPublish/data/list?key=eca2e3d1510caee33b7710a250a6f2c1&listname=Participants%7CIndividual%20Skaters&page=participants&contest=0&r=all&l=0",
            athlete_middle_url="/RRPublish/data/list?key=eca2e3d1510caee33b7710a250a6f2c1&listname=Online%7CLap%20Details&page=live&contest=0&r=pid&pid=",
            age_category_col_index=5,
            discipline_col_index=6,
            gender_col_index=7,
        ),
    ),
    2025: EventParams(
        date="2025-02-25",
        track=homestead_track,
        scraped_site_params=MyRaceResultParams(
            race_id=310199,
            ranking_home_url="https://my4.raceresult.com/310199/RRPublish/data/list?key=8d488f25d22b08ed0dc395c939995c3d&listname=Participants%7CIndividual%20Skaters&page=participants&contest=0&r=all&l=0",
            athlete_middle_url="/RRPublish/data/list?key=8d488f25d22b08ed0dc395c939995c3d&listname=Online%7CLap%20Details&page=live&contest=0&r=pid&pid=",
            age_category_col_index=4,
            discipline_col_index=5,
            gender_col_index=6,
        ),
    ),
}

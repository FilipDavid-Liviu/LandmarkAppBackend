from .base import BaseSeeder
from models import Landmark
from exceptions.exceptions import DatabaseError

class LandmarkSeeder(BaseSeeder):
    def __init__(self):
        super().__init__()
        self.dummy_data = [
            {
                "lat": 55.7526,
                "lng": 37.6211,
                "name": "St. Basil's Cathedral",
                "type": "Place of Worship",
                "description": "The Cathedral of Vasily the Blessed, commonly known as Saint Basil's Cathedral, is a church in Red Square in Moscow, Russia.",
                "image": "http://localhost:8000/static/photos/1.jpg"
            },
            {
                "lat": 48.8584,
                "lng": 2.2945,
                "name": "Eiffel Tower",
                "type": "Monument",
                "description": "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France.",
                "image": "http://localhost:8000/static/photos/2.jpg"
            },
            {
                "lat": 40.6892,
                "lng": -74.0445,
                "name": "Statue of Liberty",
                "type": "Monument",
                "description": "The Statue of Liberty is a colossal neoclassical sculpture on Liberty Island in New York Harbor in New York City.",
                "image": "http://localhost:8000/static/photos/3.jpg"
            },
            {
                "lat": 40.415853,
                "lng": 50.009168,
                "name": "Baku Ateshgah",
                "type": "Place of Worship",
                "description": "The Ateshgah of Baku is a Zoroastrian temple in Surakhani, a suburb in Baku, Azerbaijan.",
                "image": "http://localhost:8000/static/photos/4.jpg"
            },
            {
                "lat": 34.83189,
                "lng": 67.826845,
                "name": "Bamiyan Buddhas",
                "type": "Religious Monument",
                "description": "The Buddhas of Bamiyan were two 6th-century monumental statues of Gautama Buddha carved into the side of a cliff in the Bamyan valley in the Hazarajat region of central Afghanistan",
                "image": "http://localhost:8000/static/photos/5.jpg"
            },
            {
                "lat": 41.009034,
                "lng": 28.980127,
                "name": "Hagia Sophia",
                "type": "Place of Worship",
                "description": "Hagia Sophia is a former Greek Orthodox Christian patriarchal cathedral, later an Ottoman imperial mosque and now a museum in Istanbul, Turkey.",
                "image": "http://localhost:8000/static/photos/6.jpg"
            },
            {
                "lat": 34.839882,
                "lng": 134.693863,
                "name": "Himeji Castle",
                "type": "Fortification",
                "description": "Himeji Castle is a hilltop Japanese castle complex situated in the city of Himeji which is located in the Hyōgo Prefecture of Japan.",
                "image": "http://localhost:8000/static/photos/7.jpg"
            },
            {
                "lat": 51.1789,
                "lng": -1.8262,
                "name": "Stonehenge",
                "type": "Ancient Ruins",
                "description": "Stonehenge is a prehistoric monument in Wiltshire, England, two miles west of Amesbury. It consists of a ring of standing stones, each around 13 feet high, seven feet wide, and weighing around 25 tons.",
                "image": "http://localhost:8000/static/photos/8.jpg"
            },
            {
                "lat": 19.887595,
                "lng": 86.093933,
                "name": "Konark Sun Temple",
                "type": "Place of Worship",
                "description": "Konark Sun Temple is a 13th-century CE Sun Temple at Konark about 35 kilometres northeast from Puri on the coastline of Odisha, India.",
                "image": "http://localhost:8000/static/photos/9.jpg"
            },
            {
                "lat": 16.7754,
                "lng": -3.009964,
                "name": "Djinguereber Mosque",
                "type": "Place of Worship",
                "description": "The Djinguereber Mosque in Timbuktu, Mali is a famous learning center of Mali built in 1327, and cited as one of the three oldest mosques in the western Saharan region.",
                "image": "http://localhost:8000/static/photos/10.jpg"
            },
            {
                "lat": 41.8902,
                "lng": 12.4922,
                "name": "Colosseum",
                "type": "Ancient Ruins",
                "description": "The Colosseum is an oval amphitheatre in the centre of the city of Rome, Italy, the largest ancient amphitheatre ever built.",
                "image": "http://localhost:8000/static/photos/11.jpg"
            },
            {
                "lat": 29.9792,
                "lng": 31.1342,
                "name": "Great Pyramid of Giza",
                "type": "Ancient Ruins",
                "description": "The Great Pyramid of Giza is the largest of the three pyramids in the Giza pyramid complex in Egypt and one of the Seven Wonders of the Ancient World.",
            },
            {
                "lat": 37.9715,
                "lng": 23.7267,
                "name": "Parthenon",
                "type": "Ancient Ruins",
                "description": "The Parthenon is a former temple on the Athenian Acropolis, Greece, dedicated to the goddess Athena.",
            },
            {
                "lat": 39.9042,
                "lng": 116.3917,
                "name": "Forbidden City",
                "type": "Palace",
                "description": "The Forbidden City in Beijing, China, served as the imperial palace and political center of Chinese government for almost 500 years.",
            },
            {
                "lat": 35.6586,
                "lng": 139.7454,
                "name": "Tokyo Imperial Palace",
                "type": "Palace",
                "description": "The Tokyo Imperial Palace is the primary residence of the Emperor of Japan, built on the site of the former Edo Castle.",
            },
            {
                "lat": 27.1751,
                "lng": 78.0421,
                "name": "Taj Mahal",
                "type": "Religious Monument",
                "description": "The Taj Mahal is an ivory-white marble mausoleum in Agra, India, commissioned in 1632 by the Mughal emperor Shah Jahan to house the tomb of his favorite wife, Mumtaz Mahal.",
            },
            {
                "lat": 35.2992,
                "lng": 138.7861,
                "name": "Mount Fuji",
                "type": "Natural",
                "description": "Mount Fuji is the highest mountain in Japan and an active stratovolcano, considered a sacred symbol of the country.",
            },
            {
                "lat": 30.3285,
                "lng": 35.4444,
                "name": "Petra",
                "type": "Ancient Ruins",
                "description": "Petra is a famous archaeological site in Jordan, known for its rock-cut architecture and water conduit system, once the capital of the Nabataean Kingdom.",
            },
            {
                "lat": 51.5007,
                "lng": -0.1246,
                "name": "Big Ben",
                "type": "Monument",
                "description": "Big Ben is the nickname for the Great Bell of the clock at the north end of the Palace of Westminster in London, a symbol of British culture.",
            },
            {
                "lat": 27.9881,
                "lng": 86.925,
                "name": "Mount Everest",
                "type": "Natural",
                "description": "Mount Everest is the Earth's highest mountain above sea level, located in the Himalayas on the border between Nepal and China.",
            },
            {
                "lat": -13.1631,
                "lng": -72.545,
                "name": "Machu Picchu",
                "type": "Ancient Ruins",
                "description": "Machu Picchu is a 15th-century Inca citadel located in the Eastern Cordillera of southern Peru, often referred to as the 'Lost City of the Incas.'",
            },
            {
                "lat": -25.3444,
                "lng": 131.0369,
                "name": "Uluru",
                "type": "Natural",
                "description": "Uluru, also known as Ayers Rock, is a massive sandstone monolith in central Australia and a sacred site for the Anangu people.",
            },
            {
                "lat": -22.9519,
                "lng": -43.2105,
                "name": "Christ the Redeemer",
                "type": "Religious Monument",
                "description": "Christ the Redeemer is a 98-foot-tall statue of Jesus Christ in Rio de Janeiro, Brazil, and is one of the New Seven Wonders of the World.",
            },
            {
                "lat": -27.125575,
                "lng": -109.277142,
                "name": "Moai Statues of Easter Island",
                "type": "Monument",
                "description": "The Moai statues of Easter Island are massive monolithic human figures carved by the Rapa Nui people between 1250 and 1500.",
            },
            {
            "lat": 45.5146,
            "lng": 25.3676,
                "name": "Bran Castle",
                "type": "Fortification",
                "description": "Bran Castle is a historic fortress built in 1377 by Saxons."
            },
            {
                "lat": 41.011574,
                "lng": 28.983269,
                "name": "Topkapi Palace",
                "type": "Palace",
                "description": "Topkapi Palace, located in Istanbul, Turkey, served as the primary residence and administrative center of Ottoman sultans for nearly 400 years."
            },
            {
                "lat": 38.691586,
                "lng": -9.215977,
                "name": "Belém Tower",
                "type": "Fortification",
                "description": "Belém Tower is a fortification constructed between 1514 and 1520 under the direction of architect Francisco de Arruda; the tower was initially built to defend the city and later served as a lighthouse and customs house."
            },
            {
                "lat": 43.0799,
                "lng": -79.0747,
                "name": "Niagara Falls",
                "type": "Natural",
                "description": "Niagara Falls is a renowned natural wonder straddling the border between Ontario, Canada, and New York, USA."
            },
            {
                "lat": 31.7780,
                "lng": 35.2358,
                "name": "Church of the Holy Sepulchre",
                "type": "Place of Worship",
                "description": "The Church of the Holy Sepulchre is one of Christianity's holiest sites. Tradition holds that it encompasses both the location of Jesus's crucifixion at Golgotha and his empty tomb, where he was buried and resurrected."
            },
            {
                "lat": 13.4125,
                "lng": 103.8667,
                "name": "Angkor Wat",
                "type": "Place of Worship",
                "description": "Angkor Wat is a vast temple complex constructed in the early 12th century and was initially dedicated to the Hindu god Vishnu. Over time, it transitioned into a Buddhist temple."
            },
            {
                "lat": -7.6079,
                "lng": 110.2038,
                "name": "Borobudur Temple",
                "type": "Place of Worship",
                "description": "Borobudur Temple is a 9th-century Mahayana Buddhist monument and the largest of its kind in the world."
            },
            {
                "lat": 21.4225,
                "lng": 39.8262,
                "name": "Kaaba",
                "type": "Place of Worship",
                "description": "The Kaaba is Islam's holiest site. Situated at the center of the Masjid al-Haram mosque, it is a cuboid-shaped building. Covered by a black silk curtain known as the Kiswah, the Kaaba serves as the qibla, the direction Muslims face during their five daily prayers."
            }
        ]

    def seed(self):
        try:
            if self.db.query(Landmark).count() == 0:
                for data in self.dummy_data:
                    self.db.add(Landmark(**data))
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Error seeding landmarks: {str(e)}")

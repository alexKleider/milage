#!/usr/bin/env python3

klicks_in_a_mile = 1.62
litres_in_a_gallon = 3.8  # US Gallon
    # Imperial Gallon is more by 4/3.


def miles(klicks):
    return klicks/klicks_in_a_mile

def gallons(litres):
    return litres/litres_in_a_gallon

def litres_per_100_klicks(mpg):
    """
    x mpg : 1 gal => x mi
    in metric : 3.8 l => x*1.62 km
        multiply both sides by 100/(x*1.62) or (100/1.62)/x:
        3.8 l (100/1.62)/x => x*1.62 (100/1.62)/x km
        3.8 l (100/1.62)/x => 100 km
        3.8 * 100 / (x * 1.62) => 100km
        (litres_in_a_gallon * 100 / klicks_in_a_mile) / mpg <==> l/100km

    """
    return (litres_in_a_gallon * 100 / klicks_in_a_mile) / mpg


def main():
    print("15.859litres ==> {:.3f}km/100kilometers"
        .format(litres_per_100_klicks(15.859)))

if __name__ == "__main__":
    main()

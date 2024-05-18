import src.dvd_to_mkv_conversion.info_grabber as info_grabber

def argparse():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("paths", help="Paths to analyze.", nargs='+', default=[])
    parser.add_argument("-o", "--output", help="HTML output file path.", default="movie_db.html", type=str)
    args = parser.parse_args()
    return args



if __name__ == "__main__":
    args = argparse() 
    info_grabber.main(args)
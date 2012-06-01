from optparse import OptionParser


def main():
    """Entry Into Application"""
    usage = 'usage: %prog path/to/csv [options]' 
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()

    import ipdb; ipdb.set_trace()
    # open file

if __name__ == '__main__':
    main()

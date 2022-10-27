from configparser import ConfigParser


def config(filename='../env.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db_profile = {}
    if parser.has_section(section):
        all_params = parser.items(section)
        for single_param in all_params:
            db_profile[single_param[0]] = single_param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db_profile

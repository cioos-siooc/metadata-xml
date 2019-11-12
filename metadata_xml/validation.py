#!/usr/bin/env python3

from datetime import datetime


eovs = [
    'oxygen',
    'nutrients',
    'nitrate',
    'phosphate',
    'silicate',
    'inorganicCarbon',
    'dissolvedOrganicCarbon',
    'seaSurfaceHeight',
    'seawaterDensity',
    'potentialTemperature',
    'potentialDensity',
    'speedOfSound',
    'seaIce',
    'seaState',
    'seaSurfaceSalinity',
    'seaSurfaceTemperature',
    'subSurfaceCurrents',
    'subSurfaceSalinity',
    'subSurfaceTemperature',
    'surfaceCurrents'
]


def get_alternate_languge(record):
    language = record['language']
    if language == 'eng':
        return 'fra'
    if language == 'fra':
        return 'eng'


def list_intersection(lst1, lst2):
    '''Returns the intersection of two lists.
       eg list_intersection([1,2],[2,3]) returns [2]
    '''
    return list(set(lst1) & set(lst2))


def strip_elements(lst):
    'strip each element in a list of strings'
    return [e.strip() for e in lst]


acceptable_date_formats_text = ['YYYYMMDD', 'YYYY-MM-DD', 'YYYYMMDDThh:mm:ss',
                                'YYYYMMDDThhmmss']


def check_date(date_text):
    ''' gco:Date supports YYYYMMDD, YYYY-MM-DD
        gco:DateTime supports YYYYMMDDThh:mm:ss, YYYYMMDDThhmmss,
            or YYYY-MM-DDThh:mm:ss.
    '''

    acceptable_date_formats = ['%Y%m%d', '%Y-%m-%d', '%Y%m%dT%H:%M:%S',
                               '%Y%m%dT%H%M%S']

    for date_format in acceptable_date_formats:
        try:
            datetime.strptime(date_text, date_format)
            return True
        except ValueError:
            continue
    return False


def get_fields_with_bad_dates(record):
    ''' check all the date_ fields in the record and return a list of key names
        with bad dates
    '''
    bad_date_fields = []
    for field in record:
        if field.startswith('date_') and record.get(field):
            if check_date(record.get(field)) is False:
                bad_date_fields.append(field)


def join(lst):
    return ', '.join(lst)


def get_missing_fields(record):
    # required in ERDDAP: title,summary,institution,infoUrl
    mandatory_fields = [
        'language',
        'title',
        'summary',
        'institution',
        'id',
        # 'language_country',
        'keywords',
        # 'date_created',
        # 'creator_name',
        # 'creator_url',
        # 'creator_email',
        # 'project',
        # 'acknowledgement',
        # 'contributor_name',
        # 'contributor_role',
        # 'scope_code',
        # 'platform_id',
        # 'platform_role',
        # 'platform_id_authority'
    ]

    missing_fields = []

    for field in mandatory_fields:
        if field not in record:
            missing_fields.append(field)

    return missing_fields


def has_eov_in_keywords(record):
    ''' EOV check
        must be at least one EOV in the english keywords
        Also, both 'keywords' and 'keywords_<alternate_language>' must be set
    '''

    # merged english and french keywords
    keywords_alternate_lang = 'keywords_' + get_alternate_languge(record)

    all_keywords = (record.get('keywords', '').split(',')
                    + record.get(keywords_alternate_lang, '').split(','))

    return bool(list_intersection(strip_elements(all_keywords), eovs))


def get_missing_bilingual_fields(record):
    missing_fields = []
    alternate_language = get_alternate_languge(record)
    mandatory_bilingual_fields = ['title', 'summary', 'keywords']
    for field in mandatory_bilingual_fields:
        alternate_lang_field = field+'_'+alternate_language
        if alternate_lang_field not in record:
            missing_fields.append(alternate_lang_field)
    return missing_fields


progress_code_options = ['deprecated', 'proposed', 'withdrawn',
                         'notAccepted', 'accepted', 'valid', 'tentative',
                         'superseded', 'retired', 'pending', 'final',
                         'underDevelopment', 'required', 'planned', 'onGoing',
                         'obsolete', 'historicalArchive', 'completed']


def validate(record):
    ''' Validation function, throws an error or returns True
    '''

    # error messages
    errors = []

    missing_required_fields = get_missing_fields(record)

    if record.get('language') in ['eng', 'fra']:
        # some checks we can only do if 'language' is set
        missing_required_fields += get_missing_bilingual_fields(record)

        if has_eov_in_keywords(record) is False:
            errors.append(
                "There must be at least one EOV in 'keywords'."
                + "EOVs are: {}".format(join(eovs)))
    else:
        errors.append(
            "Required variable 'language' must be either 'fra' or 'eng' ")

    # check if progress_code value is in the codeList
    if ('progress_code' in record
            and record['progress_code'] not in progress_code_options):
        errors.append("progress_code must be one of: "
                      + join(progress_code_options))

    # check for badly formatted dates
    fields_with_bad_dates = get_fields_with_bad_dates(record)

    if missing_required_fields:
        errors.append(
            "Missing required fields/values: '{}'".format(
                join(missing_required_fields)))

    if fields_with_bad_dates:
        errors.append("""Date/time formatting error in field(s): {}.
                                 Pattern must match one of: {}""".format(
            join(fields_with_bad_dates), join(acceptable_date_formats_text)))

    return errors

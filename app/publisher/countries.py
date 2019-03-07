def get_countries():
    countries = [('Algeria','Algeria'),('Angola','Angola'),('Benin','Benin'),('Botswana','Botswana'),('Burkina Faso','Burkina Faso'),('Burundi','Burundi'),('Cabo Verde','Cabo Verde'),('Cameroon','Cameroon'),
    ('CAR','CAR'),('Chad','Chad'),('Comoros','Comoros'),('DRC','DRC'),('Congo','Congo'),("Cote d'Ivoire","Cote d'Ivoire"),('Djibouti','Djibouti'),('Egypt','Egypt'),('Equatorial-Guinea','Equatorial-Guinea'),
    ('Eritrea','Eritrea'),('Swaziland','Swaziland'),('Ethiopia','Ethiopia'),('Gabon','Gabon'),('Gambia','Gambia'),('Ghana','Ghana'),('Guinea','Guinea'),('Guinea-Bissau','Guinea-Bissau'),('Kenya','Kenya'),
    ('Lesotho','Lesotho'),('Liberia','Liberia'),('Libya','Libya'),('Madagascar','Madagascar'),('Malawi','Malawi'),('Mali','Mali'),('Mauritania','Mauritania'),('Mauritius','Mauritius'),('Morocco','Morocco'),
    ('Mozambique','Mozambique'),('Namibia','Namibia'),('Niger','Niger'),('Nigeria','Nigeria'),('Rwanda','Rwanda'),('Sao Tome and Principe','Sao Tome and Principe'),('Senegal','Senegal'),
    ('Seychelles','Seychelles'),('Sierra Leone','Sierra Leone'),('Somalia','Somalia'),('South Africa','South Africa'),('South Sudan','South Sudan'),('Sudan','Sudan'),('Tanzania','Tanzania'),('Togo','Togo'),
    ('Tunisia','Tunisia'),('Uganda','Uganda'),('Zambia','Zambia'),('Zimbabwe','Zimbabwe')]
    return countries


def get_arcode():
    codes={
        "Algeria": "DZ",
        "Angola" : "AO",
        "Benin"  : "BJ",
        "Botswana" : "BW",
        "Burkina Faso" : "BF",
        "Burundi":"BI",
        "Cameroon": "CM",
        "Cape Verde": "CV",
        "CAR" :"CF",
        "Chad": "TD",
        "Comoros": "KM",
        "Congo": "CG",
        "Congo": "CD",
        "Cote d'Ivoire": "CI",
        "Ivory Coast": "CI",
        "Djibouti": "DJ",
        "Egypt": "EG",
        "Equatorial Guinea":"GQ",
        "Eritrea": "ER",
        "Ethiopia": "ET",
        "Gabon": "GA",
        "Gambia":"GM",
        "Ghana": "GH",
        "Guinea": "GN",
        "Guinea-Bissau": "GW",
        "Kenya": "KE",
        "Lesotho": "LS",
        "Liberia": "LR",
        "Libyan Arab Jamahiriya":"LY",
        "Libya": "LY",
        "Madagascar": "MG",
        "Malawi": "MW",
        "Mali": "ML",
        "Mauritania": "MR",
        "Mauritius": "MU",
        "Morocco": "MA",
        "Mozambique": "MZ",
        "Namibia": "NA",
        "Niger": "NE",
        "Nigeria": "NG",
        "Rwanda":"RW",
        "Sao Tome and Principe": "ST",
        "Senegal":"SN",
        "Seychelles": "SC",
        "Sierra Leone": "SL",
        "Solomon Islands": "SB",
        "Somalia": "SO",
        "South Africa": "ZA",
        "Sudan": "SD",
        "Swaziland": "SZ",
        "Tanzania": "TZ",
        "Togo":"TG",
        "Tunisia": "TN",
        "Uganda": "UG",
        "Western Sahara": "EH",
        "Zambia": "ZM",
        "Zimbabwe": "ZW"
    }
    return codes

def get_country_code(country):
    code = get_arcode()
    try:
        county_code = code[country]
    except AttributeError:
        county_code = 'KE'
    return county_code

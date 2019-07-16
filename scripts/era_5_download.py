import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type':'reanalysis',
        'format':'grib',
        'year':[
            '2012'
        ],
        'month':[
            '01'
        ],
        'day':[
            '01','02','03',
            '04','05','06',
            '07','08','09',
            '10','11','12',
            '13','14','15',
            '16','17','18',
            '19','20','21',
            '22','23','24',
            '25','26','27',
            '28','29','30',
            '31'
        ],
        'time':[
            '00:00','01:00','02:00',
            '03:00','04:00','05:00',
            '06:00','07:00','08:00',
            '09:00','10:00','11:00',
            '12:00','13:00','14:00',
            '15:00','16:00','17:00',
            '18:00','19:00','20:00',
            '21:00','22:00','23:00'
        ],
        'variable':[
            '100m_u_component_of_wind','100m_v_component_of_wind','10m_u_component_of_neutral_wind',
            '10m_u_component_of_wind','10m_v_component_of_neutral_wind','10m_v_component_of_wind',
            '10m_wind_direction','10m_wind_gust_since_previous_post_processing','10m_wind_speed',
            '2m_dewpoint_temperature','2m_temperature','air_density_over_the_oceans'
        ]
    },
    'download.grib')

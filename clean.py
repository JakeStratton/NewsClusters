import pandas as pd 

df = pd.read_csv('data/articles_2019.csv')

#remove rows based on nan (these columns must have values, otherwise remove the row)
df = df.dropna(subset=['byline_original'])
df = df.dropna(subset=['headline_main']) 
df = df.dropna(subset=['byline_person_0_lastname'])
df = df.dropna(subset=['lead_paragraph'])

#rows to delete based on conditions
delete_cols = df[df['type_of_material'] == 'Video'].index
df.drop(delete_cols , inplace=True)

delete_cols = df[df['byline_person_1_lastname'].notnull() == True].index
df.drop(delete_cols , inplace=True)

#remove unneeded columns
columns = ['byline_original', 'multimedia_0_caption',
 'multimedia_0_credit',
 'multimedia_0_crop_name',
 'multimedia_0_height',
 'multimedia_0_legacy_xlarge',
 'multimedia_0_legacy_xlargeheight',
 'multimedia_0_legacy_xlargewidth',
 'multimedia_0_rank',
 'multimedia_0_subType',
 'multimedia_0_subtype',
 'multimedia_0_type',
 'multimedia_0_url',
 'multimedia_0_width',
 'multimedia_1_caption',
 'multimedia_1_credit',
 'multimedia_1_crop_name',
 'multimedia_1_height',
 'multimedia_1_legacy_thumbnail',
 'multimedia_1_legacy_thumbnailheight',
 'multimedia_1_legacy_thumbnailwidth',
 'multimedia_1_rank',
 'multimedia_1_subType',
 'multimedia_1_subtype',
 'multimedia_1_type',
 'multimedia_1_url',
 'multimedia_1_width',
 'multimedia_2_caption',
 'multimedia_2_credit',
 'multimedia_2_crop_name',
 'multimedia_2_height',
 'multimedia_2_rank',
 'multimedia_2_subType',
 'multimedia_2_subtype',
 'multimedia_2_type',
 'multimedia_2_url',
 'multimedia_2_width',
 'multimedia_3_caption',
 'multimedia_3_credit',
 'multimedia_3_crop_name',
 'multimedia_3_height',
 'multimedia_3_rank',
 'multimedia_3_subType',
 'multimedia_3_subtype',
 'multimedia_3_type',
 'multimedia_3_url',
 'multimedia_3_width',
 'multimedia_4_caption',
 'multimedia_4_credit',
 'multimedia_4_crop_name',
 'multimedia_4_height',
 'multimedia_4_rank',
 'multimedia_4_subType',
 'multimedia_4_subtype',
 'multimedia_4_type',
 'multimedia_4_url',
 'byline_organization',
 'byline_person',
 'byline_person_0_organization',
 'byline_person_0_qualifier',
 'byline_person_0_rank',
 'byline_person_0_title',
 'byline_person_1_middlename',
 'byline_person_1_organization',
 'byline_person_1_qualifier',
 'byline_person_1_rank',
 'byline_person_1_title',
 'byline_person_2_middlename',
 'byline_person_2_organization',
 'byline_person_2_qualifier',
 'byline_person_2_rank',
 'byline_person_2_title',
 'byline_person_3_middlename',
 'byline_person_3_organization',
 'byline_person_3_qualifier',
 'byline_person_3_rank',
 'byline_person_3_title',
 'byline_person_4_middlename',
 'byline_person_4_organization',
 'byline_person_4_qualifier',
 'byline_person_4_rank',
 'byline_person_4_title',
 'byline_person_5_middlename',
 'byline_person_5_organization',
 'byline_person_5_qualifier',
 'byline_person_5_rank',
 'byline_person_5_title',
 'byline_person_6_middlename',
 'byline_person_6_organization',
 'byline_person_6_qualifier',
 'byline_person_6_rank',
 'byline_person_6_title',
 'keywords_0_major',
 'keywords_0_rank',
 'keywords_10_major',
 'keywords_10_rank',
 'keywords_11_major',
 'keywords_11_rank',
 'keywords_12_major',
 'keywords_12_rank',
 'keywords_13_major',
 'keywords_13_rank',
 'keywords_14_major',
 'keywords_14_rank',
 'keywords_15_major',
 'keywords_15_rank',
 'keywords_16_major',
 'keywords_16_rank',
 'keywords_17_major',
 'keywords_17_rank',
 'keywords_18_major',
 'keywords_18_rank',
 'keywords_19_major',
 'keywords_19_rank',
 'keywords_1_major',
 'keywords_1_rank',
 'keywords_20_major',
 'keywords_20_rank',
 'keywords_21_major',
 'keywords_21_rank',
 'keywords_22_major',
 'keywords_22_rank',
 'keywords_23_major',
 'keywords_23_rank',
 'keywords_24_major',
 'keywords_24_rank',
 'keywords_25_major',
 'keywords_25_rank',
 'keywords_26_major',
 'keywords_26_rank',
 'keywords_27_major',
 'keywords_27_rank',
 'keywords_28_major',
 'keywords_28_rank',
 'keywords_2_major',
 'keywords_2_rank',
 'keywords_3_major',
 'keywords_3_rank',
 'keywords_4_major',
 'keywords_4_rank',
 'keywords_5_major',
 'keywords_5_rank',
 'keywords_6_major',
 'keywords_6_rank',
 'keywords_7_major',
 'keywords_7_rank',
 'keywords_8_major',
 'keywords_8_rank',
 'keywords_9_major',
 'keywords_9_rank',
 'keywords_10_name',
 'keywords_9_name',
 'keywords_8_name',
 'keywords_7_name',
 'keywords_6_name',
 'keywords_5_name',
 'keywords_4_name',
 'keywords_3_name',
 'keywords_2_name',
 'keywords_1_name',
 'keywords_0_name',
 'keywords_11_name',
 'keywords_12_name',
 'keywords_13_name',
 'keywords_14_name',
 'keywords_15_name',
 'keywords_16_name',
 'keywords_17_name',
 'keywords_18_name',
 'keywords_19_name',
 'keywords_20_name',
 'keywords_21_name',
 'keywords_22_name',
 'keywords_23_name',
 'keywords_24_name',
 'keywords_25_name',
 'keywords_26_name',
 'keywords_27_name',
 'keywords_28_name',
 'keywords_10_value',
 'keywords_11_value',
 'keywords_12_value',
 'keywords_13_value',
 'keywords_14_value',
 'keywords_15_value',
 'keywords_16_value',
 'keywords_17_value',
 'keywords_18_value',
 'keywords_19_value',
 'keywords_20_value',
 'keywords_21_value',
 'keywords_22_value',
 'keywords_23_value',
 'keywords_24_value',
 'keywords_25_value',
 'keywords_26_value',
 'keywords_27_value',
 'keywords_28_value',
 'document_type',
 'headline_content_kicker',
 'headline_kicker',
 'headline_name',
 'headline_sub',
 'headline_seo',
 'headline_print_headline',
 'multimedia_4_width',
 'slideshow_credits',
 'score',
 'byline_person_0_role',
 'byline_person_1_role',
 'byline_person_2_role',
 'byline_person_3_role',
 'byline_person_4_role',
 'byline_person_5_role',
 'byline_person_6_role',
 'snippet',
 'byline_person_1_firstname',
 'byline_person_1_lastname',
 'byline_person_2_firstname',
 'byline_person_2_lastname',
 'byline_person_3_firstname',
 'byline_person_3_lastname',
 'byline_person_4_firstname',
 'byline_person_4_lastname',
 'byline_person_5_firstname',
 'byline_person_5_lastname',
 'byline_person_6_firstname',
 'byline_person_6_lastname',
 'uri',
 'print_page',
 'Unnamed: 0'
 ]

for col in columns:
    df = df.drop(col, axis=1)

# fill missing subsection with section
df['subsectoinName'].fillna(df['section_name'], inplace=True)
df = df.reset_index()

# use first, middel, and last names to create an author column
df['byline_person_0_middlename'].fillna('None', inplace=True)
df = df.reset_index()
df['author'] = df[['byline_person_0_firstname', 'byline_person_0_middlename', 'byline_person_0_lastname']].apply(lambda x: ' '.join(x), axis=1)
df['author'] = df['author'].map(lambda x: x.replace(' None ', ' ').title())

#fill all remaining nan values - only additional keywords are missing values at this point
df = df.fillna('None')

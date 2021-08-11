import streamlit as st; import pandas as pd; import numpy as np; import spacy; import re; import json; import hashlib

st.image(
    "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/facebook/230/robot-face_1f916.png",
    width=100,
)

st.title('Mem cache v1.7 ML Engine')

uploaded_file = st.file_uploader("Upload your new project data with style", type=['csv'])

@st.cache
def load_data(nrows):
	df = pd.read_csv(uploaded_file, nrows=nrows)
	en_core = spacy.load('en_core_sci_md')

	#str
	df['Name'] = df['Name'].astype(str)
	df['City'] = df['Name'].astype(str)

	# Regex replace
	df['Department'] = df['Department'].str.replace('[^A-Za-z]', '')
	df['Name'] = df['Name'].str.replace('[^A-Za-z]', '')

	# Normalization
	df['Department'] = [entry.lower() for entry in df['Department']]
	df['Name'] = [entry.lower() for entry in df['Name']]
	df['City'] = [entry.lower() for entry in df['City']]
	df['Project Name'] = [entry.lower() for entry in df['Project Name']]

	# Lemmatization
	df['Name'] = df['Name'].apply(lambda x: " ".join([y.lemma_ for y in en_core(x)]))

	# # Append Location Data
	# longitude = []
	# latitude = []
	# def findGeocode(city):
	# 	try:
	# 		geolocator = Nominatim(user_agent="your_app_name")
	# 		return geolocator.geocode(city)
	# 	except GeocoderTimedOut:
	# 		return findGeocode(city)
	# for i in (df["City"]):
	# 	if findGeocode(i) != None:
	# 		loc = findGeocode(i)
	# 		latitude.append(loc.latitude)
	# 		longitude.append(loc.longitude)
	# 	else:
	# 		latitude.append(np.nan)
	# 		longitude.append(np.nan)
	# df["longitude"] = longitude
	# df["latitude"] = latitude
	return df



if uploaded_file is not None:
	file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
	data = load_data(1000)

	st.sidebar.write('Unique Values')
	suggest = data['Department'].unique()
	st.write()


	# st.subheader('Project Location')
	# st.map(data)

# ========= Add keys =========
if uploaded_file is not None:
	st.subheader('Dictionary updater')
	unique = data["Department"].unique()
	st.sidebar.write(unique)
	# json_key = st.sidebar.selectbox("Enter key", unique) WE NEED TO MAKE THE FIRST RENDER BLANK SOMEHOW!!!!
	col1,col2,col3=st.beta_columns(3)
	with col1:
		json_key = st.text_input("Enter key").lower()
	with col2:
	   json_value = st.text_input("Enter value").lower()
	with col3:
		json_column = st.selectbox("Column to change", ['Department'])
	
	if st.button('🗸 Append to JSON'):
		# ========= json dictionary append try 1 =========

		def add_entry(name, element):
				# return {name: {element: hashlib.md5(name.encode('utf-8')+element.encode('utf-8')).hexdigest()}}
				return {name: element}

		#add entry
		entry = add_entry(json_key, json_value)

		#Update to JSONr
		with open('elements.json', 'r') as f:
		    json_data = json.load(f)
		    print(json_data.values()) # View Previous entries
		    json_data.update(entry)

		with open('elements.json', 'w') as f:
		    f.write(json.dumps(json_data))
	col4,col5,col6=st.beta_columns([3.5,5.5,1])
	with col4:
		if st.button('✖ Delete key-value pair'):
			# ========= json dictionary delete try 1 =========
			#Update to JSONr
			with open('elements.json', 'r') as f:
				dic=json.load(f)
				print(dic.values())
				try:
					if dic[json_key]:
						del dic[json_key]
				except KeyError:
					with col5:
						st.warning('⚠️ Warning: Key doesn\'t exist!')			
				with open('elements.json', 'w') as f:
				    f.write(json.dumps(dic))
				with col6:
					st.markdown('`IDLE`')


# ========= json dictionary replace and display =========
if uploaded_file is not None:
	st.subheader('JSON Replace')
	with open('elements.json', 'r') as JSON:
		json_dict = json.load(JSON)
	json_replaced = data.replace({"Department": json_dict})
	st.write(json_replaced)

if st.button('♨ Render and append to Master'):
	st.info('Code this first bruh. That button does nothing atm')

# ========= HTML =========

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        * {font-family: "Arial Unicode MS";}
        h1, h2, h3, h4, h5, h6 {font-family: "Arial Unicode MS";}
        /* df cells header row face */
		.css-sc0g0 {font-family: "Arial Unicode MS";}
        /* df cells font face */
        .css-1l40rdr {font-family: "Arial Unicode MS";}
        .st-af {font-size: 0.9rem;}
        footer {visibility: hidden;}
        footer:after {content:'Developed with <3 by Ansh Sharma at FivD'; visibility: visible; display: block; position: relative; padding: 5px; top: 2px;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
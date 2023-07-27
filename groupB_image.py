import streamlit as st
from st_clickable_images import clickable_images
import os, glob, pathlib, random, pickle, time, requests, json, commons
import io
from io import StringIO, BytesIO
from pathlib import Path
import pandas as pd
import numpy as np
from collections import Counter
import uuid
from itertools import chain
from sftp import SFTP
from PIL import Image
hide_menu = """
<style>
#MainMenu {
    visibility:hidden;
}
</style>
"""

st.set_page_config(initial_sidebar_state="collapsed")

# set session_state for change pages
st.session_state.update(st.session_state)
if 'active_page' not in st.session_state:
    st.session_state.active_page = 'Home'
    

def save_image_tag_result(save_path, scenario, clicked, selected_tags, added_tags, options, final_aggregated_tags):
    # conv_change = []
    # for i, c in enumerate(change):
    #     target = c
    #     if c == "-":
    #         target = selected_tags[i]
    #     conv_change.append(target)
    # print(conv_change)
    results_B = {'Scenario': scenario, 'Image': f"{str(int(clicked)+1)}", 'Selected image tags': selected_tags, 'Added tags': added_tags, 'Added image number': options, 'Final aggregated tags': final_aggregated_tags}
    if not os.path.exists(save_path):
        data = {}
        data['submits'] = []
        data['submits'].append(results_B)
        print("no exists", data)
        with open(save_path, 'w') as save_f:
            json.dump(data, save_f, ensure_ascii=False, indent=4)

    else:
        data = {}
        with open(save_path, "r") as json_file:
            data = json.load(json_file)
        data['submits'].append(results_B)
        print("exists, before", data)

        with open(save_path, "w") as save_f:
            json.dump(data, save_f, ensure_ascii=False, indent=4)
            print("exists, after", data)

def save_music_suitability_result(save_path, satis_result):
    results_A = {'Satis_result': satis_result}
    if not os.path.exists(save_path):
        data = {}
        data['submits'] = []
        data['submits'].append(results_A)
        print("no exists", data)
        with open(save_path, 'w') as save_f:
            json.dump(data, save_f, ensure_ascii=False, indent=4)

    else:
        data = {}
        with open(save_path, "r") as json_file:
            data = json.load(json_file)
        data['submits'].append(results_A)
        print("exists, before", data)

        with open(save_path, "w") as save_f:
            json.dump(data, save_f, ensure_ascii=False, indent=4)
            print("exists, after", data)

# callback functions for change page
def CB_Home():
    st.session_state.active_page = 'Page_1'

# def CB_Page0():
#     st.session_state.active_page = 'Page_1'

def CB_Page1(save_path, scenario, clicked, selected_tags, added_tags, options, final_aggregated_tags):
    save_image_tag_result(save_path, scenario, clicked, selected_tags, added_tags, options, final_aggregated_tags)
    music_retrieval()
    st.session_state.active_page = 'Page_2'

def CB_Page2(save_path, satis_result):
    save_music_suitability_result(save_path, satis_result)
    st.session_state.active_page = 'Page_3'

def CB_Page3(save_path, scenario, clicked, selected_tags, added_tags, options, final_aggregated_tags):
    save_image_tag_result(save_path, scenario, clicked, selected_tags, added_tags, options, final_aggregated_tags)
    music_retrieval()
    st.session_state.active_page = 'Page_4'

def CB_Page4(save_path, satis_result):
    save_music_suitability_result(save_path, satis_result)
    st.session_state.active_page = 'Page_5'

def CB_Page5(save_path, scenario, clicked, selected_tags, added_tags, options, final_aggregated_tags):
    save_image_tag_result(save_path, scenario, clicked, selected_tags, added_tags, options, final_aggregated_tags)
    music_retrieval()
    st.session_state.active_page = 'Page_6'

def CB_Page6(save_path, satis_result):
    save_music_suitability_result(save_path, satis_result)
    st.session_state.active_page = 'Page_9'

# def CB_Page7(save_path, clicked, selected_tags, satis_result, change):
#     save_image_tag_result(save_path, clicked, selected_tags, satis_result, change)
#     music_retrieval()
#     st.session_state.active_page = 'Page_8'

# def CB_Page8():
#     st.session_state.active_page = 'Page_9'

def CB_Page9():
    st.session_state.active_page = 'Page_10'


sftp = SFTP(st.secrets["HOSTNAME"], st.secrets["USERNAME"], st.secrets["PASSWORD"])

def home():
    id = str(uuid.uuid4())
    st.session_state['id'] = id
    result_file_name = id + ".json"
    save_path = get_result_dir() + "/" + result_file_name
    
    header = st.container()
    with header:
        title = st.title("Let's find music! 🎵")
        st.markdown(hide_menu, unsafe_allow_html = True)

        sh1 = st.container()
        with sh1:
            subheader2 = st.subheader('🧪 In this experiment:')
            st.markdown("In this experiment, participants will try out the music search system.") 
            st.markdown("Our system searches for music that fits your mood or specific situation.")
            st.markdown("- STEP 1: We provide three scenarios and multiple images.")
            st.markdown("- STEP 2: First, please select your preferred scenario from the three provided options, and click on the image that best represents the scenario.")
            st.markdown("- STEP 3: Our system automatically detects images similar to the one you select.")
            st.markdown("- STEP 4: You can add similar images to make your search more accurate.")
            st.markdown("- STEP 5: Now, please enjoy the searched music.")
            st.markdown("- STEP 6: Repeat the process two more times.")
            st.write('-----')


        sh2 = st.container()
        with sh2:
            subheader3 = st.subheader('👀 Caution')
            st.markdown("- **Please read the description carefully and follow the instructions. If you skip steps, your participation in the experiment may not be complete.**")
            # st.caption("- 시스템이 작동되지 않거나, 오류 메시지가 표시될 경우 손을 들어 연구자에게 알려주세요.")
            st.markdown("- **The searched music is copyright-free music provided for research purposes.**")
            st.markdown("- Therefore, please note that <span style='color:red'> the searched music may be different from the latest music you are familiar with.</span>",unsafe_allow_html=True)
            st.write('-----')

        st.experimental_set_query_params(path=save_path)
        st.button('Agree, Start', on_click=CB_Home)
 

 ## ------------------ Instruction warning ----------------------------
# def note():
#     st.markdown(hide_menu, unsafe_allow_html = True)
#     image = Image.open('note.png')
#     st.image(image, caption='Caution', width = 1000)

#     st.button('Confirmed', on_click=CB_Page0)
 ## ------------------ for Mood Image Retrieval ------------------------ 
def get_result_dir():
    path = os.getcwd() + "/results"
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    print("created result dir: " + path)
    return path

mood_imgs = [
                'https://github.com/ppjjee/MuFiB/blob/main/images/adventure_summer_fast.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/images/sad_calm_emotional.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/images/holiday_melodic_corporate.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/images/space_background_love.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/images/calm.jpg?raw=true',       
                'https://github.com/ppjjee/MuFiB/blob/main/images/holiday_romantic_party.jpg?raw=true', # 1번째로 이동
                'https://github.com/ppjjee/MuFiB/blob/main/images/calm_relaxing.jpg?raw=true', # 1번째로 이동      
                'https://github.com/ppjjee/MuFiB/blob/main/images/relaxing.jpg?raw=true', # 1번째로 이동
                'https://github.com/ppjjee/MuFiB/blob/main/images/party.jpg?raw=true', # 1번째로 이동
                'https://github.com/ppjjee/MuFiB/blob/main/images/holiday_party_summer.jpg?raw=true', # 1번째로 이동
            ]
mood_imgs2 = [
                'https://github.com/ppjjee/MuFiB/blob/main/images/dream_positive_happy.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/images/love_positive.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/images/sad_melancholic_calm.jpg?raw=true', # 2번째로 이동
                'https://github.com/ppjjee/MuFiB/blob/main/images/children_game_fun.jpg?raw=true', # 2번째로 이동
                'https://github.com/ppjjee/MuFiB/blob/main/images/corporate.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/images/children.jpg?raw=true', # 2번째로 이동
                'https://github.com/ppjjee/MuFiB/blob/main/images/calm_motivational.jpg?raw=true', # 2번째로 이동
                'https://github.com/ppjjee/MuFiB/blob/main/images/nature_dark.jpg?raw=true', # 2번째로 이동
                'https://github.com/ppjjee/MuFiB/blob/main/images/melancholic.jpg?raw=true', # 2번째로 이동
            ]           
theme_imgs = [
                'https://github.com/ppjjee/MuFiB/blob/main/images/trailer_adventure_commercial.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/images/relaxing_calm.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/images/melodic_positive.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/images/adventure_meditative.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/images/melodic_happy_adventure.jpg?raw=true', # 3번째로 이동
                'https://github.com/ppjjee/MuFiB/blob/main/images/nature.jpg?raw=true', # 3번째로 이동
                'https://github.com/ppjjee/MuFiB/blob/main/images/adventure_trailer_commercial.jpg?raw=true', # 3번째로 이동
                'https://github.com/ppjjee/MuFiB/blob/main/images/dark.jpg?raw=true', #3번째로 이동
                'https://github.com/ppjjee/MuFiB/blob/main/images/commercial_film_happy.jpg?raw=true', # 3번째로 이동
            ]
# theme_imgs2 = [
#                 'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/children.jpg?raw=true',
#                 'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/commercial_advertising_corporate.jpg?raw=true',
#                 'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/film.jpg?raw=true',
#                 'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/game.jpg?raw=true',
#                 'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/love.jpg?raw=true',
#                 'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/movie_background_film.jpg?raw=true',
#                 'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/nature_dark.jpg?raw=true',
#                 'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/space.jpg?raw=true',
#                 'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/sport_action_adventure.jpg?raw=true',
#                 'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/summer_holiday_travel.jpg?raw=true',
#             ]
music_tags = [
    '-', 'action', 'adventure', 'advertising', 'background', 'ballad', 'calm', 'children', 'christmas', 'commercial', 'cool', 'corporate',
    'dark', 'deep', 'documentary', 'drama', 'dramatic', 'dream', 'emotional', 'energetic', 'epic', 'fast', 'film', 'fun', 'funny', 'game',
    'groovy', 'happy', 'heavy', 'holiday', 'hopeful', 'inspiring', 'love', 'meditative', 'melancholic', 'melodic', 'motivational',
    'movie', 'nature', 'party', 'positive', 'powerful', 'relaxing', 'retro', 'romantic', 'sad', 'sexy', 'slow', 'soft', 'soundscape', 
    'space', 'sport', 'summer', 'trailer', 'travel', 'upbeat', 'uplifting'
    ]

def image_page1(imgs, cb):
    # show frontend title 
    st.title("Let's find music!")
    st.markdown("✔️ STEP 1: Please select your preferred scenario from the three provided options, and click on the image that best represents the scenario.")
    # st.markdown("✔️ Please select a sample image. We recommend music that matches the selected image.")
    scenario = st.radio(
    "Please select a scenario that you preferred the most.",
    ('Feeling tired but unable to sleep.', 
    'During exercise (yoga or fitness, etc.).', 
    'Preparing for a party.'))
    st.markdown("✔️ STEP 2: Click on the image that best represents your selected scenario. We will find music that matches your chosen image.")
    st.markdown("✔️ STEP 3: After selecting an image, please wait for a while until the next process.")
    
    st.markdown(hide_menu, unsafe_allow_html = True)

    save_path = st.experimental_get_query_params()['path'][0]

    # show imgs to be selected    
    selection = st.container()
    with selection:
        model_load_state = st.info('👉 We are working on it...! 👀')
        try:
            all_tags = []
            tag_list = []
            for i in imgs:
                a= i.split('/')[-1]
                b = a.split('?')[0]
                c = b.split('.')[0]
                tag_list.append(c)

            for j in tag_list:
                a = j.split('_')
                all_tags.append(a)
        
            # display images that can be clicked on using 'clickable_images' func
            clicked = clickable_images(paths=imgs, 
                                        titles=[f"Sample #{str(i)}" for i in range(1, len(imgs)+1)],
                                        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                                        img_style={"margin": "5px", "height": "200px"})  
            
            model_load_state.success('After clicking an image you like, scroll down to see similar images to the one you selected.')
            
                
            # if some image is clicked,
            if clicked > -1:
                model_load_state.info(f"**Images similar to sample #{str(int(clicked)+1)} are bellow.**")
                selected_tags = all_tags[clicked]
                
                if len(selected_tags) == 2:
                    selected_tags.append('-')
                elif len(selected_tags) == 1:
                    selected_tags.append('-')
                    selected_tags.append('-')

                st.write('-----')
                st.subheader(f"Images similar to sample #{str(int(clicked)+1)} are below.")
                st.info(f'✔️If you want to enlarge the image, mouse over the image and click on the expand icon.') 

                # 유사 이미지 보여주기
                similar_images = {0:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/dark_rSfuFUb-zD8.jpg?raw=true', # /nas3/epark/workspace/retreival/unsplash_data_merge_new/dark_rSfuFUb-zD8.jpg
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/summer_m-3BcC8xSWo.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/adventure_UiEPEzSwf5Y.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/fast_OnmDVnyofVM.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/summer_vSfefVjrGz4.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/action_IQdMxDnhuzI.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/adventure_q9rpNOd1hcI.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/film_aCX-pyyczyE.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/adventure_2G4XSjqzMyk.jpg?raw=true'], 
                1:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/dramatic_M1o0YeTvb0w.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_o364nYBlfvI.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/sad_rVxwmum9Rjs.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/drama_JWZHw_FXxFM.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/dark_xd9ki66m_AA.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/emotional_sO6yji4O_FI.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_werrs0UfZvU.jpg?raw=true'], 
                2:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/melodic_DXHog7Ktrwg.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/retro_zKaTW0Jv4jM.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/energetic_31HS1aQ1tMw.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_t-j4MkVyqFQ.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/melodic_8fbXv0PW6qk.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/melodic_P1NCcANxyYQ.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/corporate__ssmNHkymiA.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/melodic_Visxcphdymk.jpg?raw=true'], 
                3:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/love_-1qIRIqN14A.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/love_E8FaHPExFNg.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/melodic_3hiVgZkxr7g.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/background_SQ1kv2upHbc.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/background_Z1A2U0vo8uY.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/background_XL5ysBNBV5I.jpg?raw=true'], 
                4:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_0214ke7k2dI.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/groovy_4XJcFMeBoZc.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/meditative_1GrlsYupLP8.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_IwI0g4ef9cQ.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_QEZOlAZXWq0.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_zdShIOOI3_4.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_QmTeMHweRp8.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_kUqJ5Kf14JA.jpg?raw=true'],
                5:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/party_VBsG1VOgLIU.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/game_Yl7Y8DhyzyY.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/holiday_Cf-iAhAiqwo.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/cool_VUKlc1KDLwo.jpg?raw=true', 
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/soft_63IDHmoQpL0.jpg?raw=true', 
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/party_W9GvbwOd120.jpg?raw=true', 
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/party_zYfFGI3Xw7M.jpg?raw=true', ##children
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/romantic__afBES698bA.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/holiday_Qf17ez87hLg.jpg?raw=true'],
                6:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_Ve3hWAANHSU.jpg?raw=true', 
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/relaxing_OZiflZqq0N0.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/relaxing_FYaaWYcbPOY.jpg?raw=true', ##retro
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/relaxing_4Wlp6m8hroE.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/relaxing_0Ymt53tBapQ.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/relaxing_4DxjAJxXE7c.jpg?raw=true'],
                7:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/adventure_JHxBeZfIsck.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/relaxing_dvl4C_4S9Q0.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/cool_VLWuCo6H7h8.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/travel_qrjCpGh5td0.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_RPcIkOzN0iQ.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/relaxing_LrvqwqEzxa4.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/travel_S9ts_A3-khk.jpg?raw=true',##children
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/relaxing_hArsf0-tVj8.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/travel_foPx39kj7Rw.jpg?raw=true'],
                8:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/party_GIXpWit5kY0.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/happy_FgHvCcj3Jus.jpg?raw=true', ##dark
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/party_eyFGaU4vKog.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/party_Wm-GDBlJU8k.jpg?raw=true', ##movie
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/party_hl0yBiB4i5M.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/happy_rnNFHYzz0Ww.jpg?raw=true', ##christmas
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/party_Ie_dMMsT_Ww.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/christmas_VlXBwLZ_L94.jpg?raw=true'],
                9:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/holiday_z2esruz6gtU.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/summer_c29cb9moISE.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/groovy_U_pZityO2oo.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/retro_JS3aOzdzBsI.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/holiday_xAHfhMcsAc8.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/party_ZFBx9mWbYQs.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/party_5JtuW6PqGKE.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/holiday_hiG9H-qybaw.jpg?raw=true'],
                }

                ## 함수로 만들기!!!!
                cols = st.columns(10)
                def tag_selector (sim_images, clicked_images):
                    for k, v in sim_images.items():
                        if clicked_images == k:
                            for i in range(len(sim_images[clicked_images])):
                                try:
                                    cols[i].markdown(f'Image #'+str(i+1))
                                    cols[i].image(v[i], use_column_width=True)
                                except IndexError:
                                    pass
                                continue
                            else:
                                print(clicked_images)

                    length = len(sim_images[clicked_images])
                    return length
                
                length = tag_selector(similar_images, clicked)
                ## 함수 콜백
                # if st.session_state.active_page == 'Page_1':
                #     length = tag_selector(similar_images, clicked)
                # elif st.session_state.active_page == 'Page_3':
                #     length = tag_selector(similar_images2, clicked)
                # elif st.session_state.active_page == 'Page_5':
                #     length = tag_selector(similar_images3, clicked)

                options = st.multiselect(
                    'Add images that expresses similar mood or situation. If there is no similar image, or if you want to search music directly without selecting a similar image, please click the next button below.',
                    list(range(1, length+1))
                )
                print('Added image numbers are:', options)
                

                def adding_tags(sim_images, clicked_images, options):
                    added_tags = []
                    for i in options:
                        a = sim_images[clicked_images][i-1] #1부터 받기 때문에 실제로는 -1을 해주어야 list 값과 일치함
                        b = a.split('/')[-1]
                        c = b.split('_')[0]
                        added_tags.append(c)
                    print('added tags are:', added_tags)
                    return added_tags
                
                added_tags = adding_tags(similar_images, clicked, options)
                ## 함수 콜백
                # if st.session_state.active_page == 'Page_1':
                #     added_tags = adding_tags(similar_images, clicked, options)
                # elif st.session_state.active_page == 'Page_3':
                #     added_tags = adding_tags(similar_images2, clicked, options)
                # elif st.session_state.active_page == 'Page_5':
                #     added_tags = adding_tags(similar_images3, clicked, options)

                ####################################################
                aggregated_tags= list(set(selected_tags) | set(added_tags))
                if '-' in aggregated_tags:
                    aggregated_tags.remove('-')
                else:
                    pass
                print('mood/theme aggregated tags are:', aggregated_tags)

                genre_tags = {'background':'easylistening','film':'soundtrack', 'melancholic':'ambient', 'children': 'soundtrack', 'relaxing': 'classical',
                'meditative': 'classical', 'cool': 'electronic', 'emotional': 'classical', 'documentary': 'soundtrack', 'love': 'pop', 
                'drama': 'soundtrack', 'adventure': 'orchestral', 'heavy': 'metal', 'dark': 'ambient', 'retro': 'pop', 'ballad': 'pop',
                'epic': 'classical', 'calm': 'classical', 'slow': 'experimental', 'energetic':'electronic', 'deep': 'house', 'inspiring':'easylistening',
                'soft': 'easylistening', 'space': 'electronic', 'fun': 'pop', 'horror': 'soundtrack', 'positive':'pop', 'happy':'pop', 'summer':'chillout',
                'dream':'ambient', 'romantic':'easylistening', 'sad':'classical', 'hopeful':'easylistening', 'motivational':'pop', 
                'uplifting': 'pop', 'party':'dance','mellow':'chillout', 'groovy':'pop', 'soundscape':'ambient', 'corporate':'pop', 
                'advertising':'soundtrack','sport':'rock', 'sexy':'lounge', 'fast':'electronic', 'nature':'ambient', 'commercial':'pop', 
                'funny':'dance','dramatic':'orchestral', 'holiday':'pop', 'ambiental':'soundtrack', 'christmas':'pop', 'game':'electronic', 
                'travel':'pop','powerful':'rock', 'upbeat':'hiphop', 'movie':'soundtrack', 'action':'rock', 'trailer':'trailer'}
                    
                keywords_associated_genre = []
                for i in aggregated_tags:
                    for k, v in genre_tags.items():
                        if i in k:
                            keywords_associated_genre.append(v)
                        else:
                            pass
                print('The keyword related to the genre are:', keywords_associated_genre)

                final_aggregated_tags= list(set(aggregated_tags) | set(keywords_associated_genre))
                print('Final aggregated tags are:', final_aggregated_tags)

                st.experimental_set_query_params(path=save_path)
                st.button('NEXT', on_click=cb, args=(save_path, scenario, clicked, selected_tags, options, added_tags, final_aggregated_tags))


            else:
                model_load_state.info(f"**Please select a preferred scenario first, and click on the image that best represents the scenario.**")
                
        except Exception as e:
            print("Oops!", e.__class__, "occurred.")
            print(e)
            message_container = st.empty() 
            message = message_container.write('👉 Please, wait. We are working on it...! 👀')
            if message != '':
                message_container.empty()


## ------------------ image second page ------------------------------
def image_page2(imgs, cb):
    # show frontend title 
    st.title("Let's find music!")
    st.markdown("✔️ STEP 1: Please select your preferred scenario from the three provided options, and click on the image that best represents the scenario.")
    # st.markdown("✔️ Please select a sample image. We recommend music that matches the selected image.")
    scenario = st.radio(
    "Please select a scenario that you preferred the most.",
    ('Want to discover a new music.', 
    'Playing with a child.', 
    'Studying or working.'))
    st.markdown("✔️ STEP 2: Click on the image that best represents your selected scenario. We will find music that matches your chosen image.")
    st.markdown("✔️ STEP 3: After selecting an image, please wait for a while until the next process.")

    st.markdown(hide_menu, unsafe_allow_html = True)

    save_path = st.experimental_get_query_params()['path'][0]

    # show imgs to be selected    
    selection = st.container()
    with selection:
        model_load_state = st.info('👉 We are working on it...! 👀')
        try:
            all_tags = []
            tag_list = []
            for i in imgs:
                a= i.split('/')[-1]
                b = a.split('?')[0]
                c = b.split('.')[0]
                tag_list.append(c)

            for j in tag_list:
                a = j.split('_')
                all_tags.append(a)
        
            # display images that can be clicked on using 'clickable_images' func
            clicked = clickable_images(paths=imgs, 
                                        titles=[f"Sample #{str(i)}" for i in range(1, len(imgs)+1)],
                                        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                                        img_style={"margin": "5px", "height": "200px"})  
            
            model_load_state.success('After clicking an image you like, scroll down to see similar images to the one you selected.')
            
                
            # if some image is clicked,
            if clicked > -1:
                model_load_state.info(f"**Images similar to sample #{str(int(clicked)+1)} are bellow.**")
                selected_tags = all_tags[clicked]
                
                if len(selected_tags) == 2:
                    selected_tags.append('-')
                elif len(selected_tags) == 1:
                    selected_tags.append('-')
                    selected_tags.append('-')

                st.write('-----')
                st.subheader(f"Images similar to sample #{str(int(clicked)+1)} are below.")
                st.info(f'✔️If you want to enlarge the image, mouse over the image and click on the expand icon.') 

                # 유사 이미지 보여주기
                similar_images2 = {0:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/melodic_S0oqXncDqP8.jpg?raw=true', ## action
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/dream_CetnsEMUydc.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/cool_4zXx50JLTnY.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/positive_JQXe2vrbNOA.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/film_j4cOKZojvNI.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/soft_fsbfVrhpV6k.jpg?raw=true', ##christmas
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/happy_ewH71a1zdmA.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/soft_jGVySnyIPXc.jpg?raw=true'], 
                1:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/love_ZshVGzJ6a_s.jpg?raw=true', ##cool
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/cool_WtFvRYuS7wc.jpg?raw=true', ##adventure
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/motivational_Oy2DiS1XXGc.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/love_XLFKpzK8m_Q.jpg?raw=true', 
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/motivational_TpaWqZrSP1o.jpg?raw=true'], ##sport
                2:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/nature_qJmfb_wWXhw.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/nature_60XLoOgwkfA.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/sad_p_-bbbzy87s.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/sad_exI3uXWZgwo.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_KhPtWXmV-cY.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/film__o2kocC8kiY.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/background_XfG2S7ca7hI.jpg?raw=true'],
                3:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/happy_rxB0L6nrP5M.jpg?raw=true', # children_game
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/game_eLZJTFPCfA8.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/children_Un8NnnQOMfA.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/children_3BztcJxliEM.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/funny_Uz5nEXMceSk.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/fun_04-RGWREZaU.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/game_LjAAUZadNrg.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/game_FEhFnQdLYyM.jpg?raw=true'],
                4:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/corporate_s6w5NOxtm7U.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/corporate_a7A9O5htrKs.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/corporate___DIXb69qyY.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/corporate_CPs2X8JYmS8.jpg?raw=true',],
                5:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/children_ZSsJBGhor6I.jpg?raw=true', #children
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/happy_3ShDt858xes.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/party_phm8rn2thkk.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/fun_F8G44Qm_lCA.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/fun_buN4aX5JaNs.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/children_FCxZ0hDm4FA.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/children_dtSm9l9GlHE.jpg?raw=true'],
                6:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/retro_yZVBebc1GnE.jpg?raw=true', # retro_motivational
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_6URZVbb7r-c.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_DjJ49s6uD2o.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/motivational_B4Ngz_pdvz4.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_XNwy-SuaH4M.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/meditative_AigO5TWibjk.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/meditative_4Gi3H-4evlk.jpg?raw=true'],
                7:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/dark_nn9qPOjPNag.jpg?raw=true', #nature_dark
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/nature_ZBi4YhdiyPo.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/trailer_Rv9j87zTc_E.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/nature_qOktg322Byw.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/dark_w-lINiHiH64.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/deep_Q6tmUuUSCkc.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/deep_--kGuWTwn48.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_yxJs9n5W3Ns.jpg?raw=true'],
                8:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/melancholic_Q0yUoNhAR04.jpg?raw=true', #trailer_melancholic
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/dark_yF9yF94sLoM.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/dark_Qs5cp4NARUQ.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/dark_cnAmaEgSRsU.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/melancholic_H8dDVFCqeKA.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/background_4kYCGOyMsiQ.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/melancholic_eow7_24T-gU.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/dark_0cZj4pz1VW0.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_JgiYHgWU0Do.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/dark_nkXDGnqFb7g.jpg?raw=true'],
                }
                
                ###################################################
                ## 함수로 만들기!!!!
                cols = st.columns(10)
                def tag_selector (sim_images, clicked_images):
                    for k, v in sim_images.items():
                        if clicked_images == k:
                            for i in range(len(sim_images[clicked_images])):
                                try:
                                    cols[i].markdown(f'Image #'+str(i+1))
                                    cols[i].image(v[i], use_column_width=True)
                                except IndexError:
                                    pass
                                continue
                            else:
                                print(clicked_images)

                    length = len(sim_images[clicked_images])
                    return length
                
                length = tag_selector(similar_images2, clicked)
                ## 함수 콜백
                # if st.session_state.active_page == 'Page_1':
                #     length = tag_selector(similar_images, clicked)
                # elif st.session_state.active_page == 'Page_3':
                #     length = tag_selector(similar_images2, clicked)
                # elif st.session_state.active_page == 'Page_5':
                #     length = tag_selector(similar_images3, clicked)

                options = st.multiselect(
                    'Add images that expresses similar mood or situation. If there is no similar image, or if you want to search music directly without selecting a similar image, please click the next button below.',
                    list(range(1, length+1))
                )
                print('Added image numbers are:', options)
                

                def adding_tags(sim_images, clicked_images, options):
                    added_tags = []
                    for i in options:
                        a = sim_images[clicked_images][i-1] #1부터 받기 때문에 실제로는 -1을 해주어야 list 값과 일치함
                        b = a.split('/')[-1]
                        c = b.split('_')[0]
                        added_tags.append(c)
                    print('added tags are:', added_tags)
                    return added_tags
                
                added_tags = adding_tags(similar_images2, clicked, options)
                ## 함수 콜백
                # if st.session_state.active_page == 'Page_1':
                #     added_tags = adding_tags(similar_images, clicked, options)
                # elif st.session_state.active_page == 'Page_3':
                #     added_tags = adding_tags(similar_images2, clicked, options)
                # elif st.session_state.active_page == 'Page_5':
                #     added_tags = adding_tags(similar_images3, clicked, options)

                ####################################################
                aggregated_tags= list(set(selected_tags) | set(added_tags))
                if '-' in aggregated_tags:
                    aggregated_tags.remove('-')
                else:
                    pass
                print('mood/theme aggregated tags are:', aggregated_tags)

                genre_tags = {'background':'easylistening','film':'soundtrack', 'melancholic':'ambient', 'children': 'soundtrack', 'relaxing': 'classical',
                'meditative': 'classical', 'cool': 'electronic', 'emotional': 'classical', 'documentary': 'soundtrack', 'love': 'pop', 
                'drama': 'soundtrack', 'adventure': 'orchestral', 'heavy': 'metal', 'dark': 'ambient', 'retro': 'pop', 'ballad': 'pop',
                'epic': 'classical', 'calm': 'classical', 'slow': 'experimental', 'energetic':'electronic', 'deep': 'house', 'inspiring':'easylistening',
                'soft': 'easylistening', 'space': 'electronic', 'fun': 'pop', 'horror': 'soundtrack', 'positive':'pop', 'happy':'pop', 'summer':'chillout',
                'dream':'ambient', 'romantic':'easylistening', 'sad':'classical', 'hopeful':'easylistening', 'motivational':'easylistening', 
                'uplifting': 'pop', 'party':'dance','mellow':'chillout', 'groovy':'pop', 'soundscape':'ambient', 'corporate':'pop', 
                'advertising':'soundtrack','sport':'rock', 'sexy':'lounge', 'fast':'electronic', 'nature':'ambient', 'commercial':'pop', 
                'funny':'dance','dramatic':'orchestral', 'holiday':'pop', 'ambiental':'soundtrack', 'christmas':'pop', 'game':'electronic', 
                'travel':'pop','powerful':'rock', 'upbeat':'hiphop', 'movie':'soundtrack', 'action':'rock', 'trailer':'trailer'}
                    
                keywords_associated_genre = []
                for i in aggregated_tags:
                    for k, v in genre_tags.items():
                        if i in k:
                            keywords_associated_genre.append(v)
                        else:
                            pass
                print('The keyword related to the genre are:', keywords_associated_genre)

                final_aggregated_tags= list(set(aggregated_tags) | set(keywords_associated_genre))
                print('Final aggregated tags are:', final_aggregated_tags)

                if 'children' in final_aggregated_tags:
                    final_aggregated_tags = ['children', 'fun']
                    print('Choose children scenario: changed final aggregated tags:', final_aggregated_tags)

                st.experimental_set_query_params(path=save_path)
                st.button('NEXT', on_click=cb, args=(save_path, scenario, clicked, selected_tags, added_tags, options, final_aggregated_tags, ))


            else:
                model_load_state.warning(f"**⚠️There is no image selected. Please select a sample image.**")
                
        except Exception as e:
            print("Oops!", e.__class__, "occurred.")
            print(e)
            message_container = st.empty() 
            message = message_container.write('👉 Please, wait. We are working on it...! 👀')
            if message != '':
                message_container.empty()
## ---------------------- Image third page ---------------------------
def image_page3(imgs, cb):
    # show frontend title 
    st.title("Let's find music!")
    st.markdown("✔️ STEP 1: Please select your preferred scenario from the three provided options, and click on the image that best represents the scenario.")
    # st.markdown("✔️ Please select a sample image. We recommend music that matches the selected image.")
    scenario = st.radio(
    "Please select a scenario that you preferred the most.",
    ('Commuting to and from work.', 
    'While driving or before driving.', 
    'Emotional early morning hours.'))
    st.markdown("✔️ STEP 2: Click on the image that best represents your selected scenario. We will find music that matches your chosen image.")
    st.markdown("✔️ STEP 3: After selecting an image, please wait for a while until the next process.")

    st.markdown(hide_menu, unsafe_allow_html = True)

    save_path = st.experimental_get_query_params()['path'][0]

    # show imgs to be selected    
    selection = st.container()
    with selection:
        model_load_state = st.info('👉 We are working on it...! 👀')
        try:
            all_tags = []
            tag_list = []
            for i in imgs:
                a= i.split('/')[-1]
                b = a.split('?')[0]
                c = b.split('.')[0]
                tag_list.append(c)

            for j in tag_list:
                a = j.split('_')
                all_tags.append(a)
        
            # display images that can be clicked on using 'clickable_images' func
            clicked = clickable_images(paths=imgs, 
                                        titles=[f"Sample #{str(i)}" for i in range(1, len(imgs)+1)],
                                        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                                        img_style={"margin": "5px", "height": "200px"})  
            
            model_load_state.success('After clicking an image you like, scroll down to see similar images to the one you selected.')
            
                
            # if some image is clicked,
            if clicked > -1:
                model_load_state.info(f"**Images similar to sample #{str(int(clicked)+1)} are bellow.**")
                selected_tags = all_tags[clicked]
                
                if len(selected_tags) == 2:
                    selected_tags.append('-')
                elif len(selected_tags) == 1:
                    selected_tags.append('-')
                    selected_tags.append('-')

                st.write('-----')
                st.subheader(f"Images similar to sample #{str(int(clicked)+1)} are below.")
                st.info(f'✔️If you want to enlarge the image, mouse over the image and click on the expand icon.') 

                # 유사 이미지 보여주기              
                similar_images3 = {0:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/adventure_9aUQlS6Pgns.jpg?raw=true', # trailer_adventure_commercial
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/trailer_w8kIQEU34Po.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/energetic_VK2KjAfvOPs.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/trailer_ktltWUbd1lk.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_RKf6vgN12qM.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/commercial_zmBfXGF6Otg.jpg?raw=true'],
                1:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/relaxing_IgomcyU3PCs.jpg?raw=true', #relaxing_calm
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/relaxing_VfWYEniF5K8.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm__GAfRnQzXA4.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_Urh0w8Rpwpg.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/relaxing_if6hfEkqFNk.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/calm_aPJif68ghkg.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/love_1xzSAlZUVSc.jpg?raw=true'],
                2:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/melodic_DiNNWOqplfU.jpg?raw=true', #melodic
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/melodic_jJGc21mEh8Q.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/melodic_9nQwnympSfw.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/upbeat_OsgLI_awdk0.jpg?raw=true'], 
                3:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/adventure_h0Af70v6p0o.jpg?raw=true', #adventure_meditative
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/meditative_eA2t5EvcxU4.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/uplifting_w28Ei0Ap96w.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/sad_gQ3NgmHj5tY.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/adventure_qIzSE8QcXkE.jpg?raw=true'],
                4:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/melodic_Z-4RFLosaMs.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/adventure_FlFHP9kNeuE.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/melodic_bxq2uYtDCLk.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/happy_qScXkp4uBXU.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/adventure_qymfP660rCI.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/film_nyFSRz02-mQ.jpg?raw=true'],
                5:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/nature_jwTvCQQJXh0.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/dark_gnLlGA1D8oI.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/nature_pNnUJEN2zns.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/nature_Z6IKZFJA2wQ.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/nature_xY_6ZENqcfo.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/nature_c5IvumengsE.jpg?raw=true'],
                6:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/film_ZHgOc2qss3U.jpg?raw=true', 
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/trailer_bmZljCM1ue8.jpg?raw=true', 
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/holiday_Jojw4XIOmVI.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/adventure_0SURIr_updA.jpg?raw=true', 
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/trailer_z7pUqeJNWww.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/commercial_v8PPgZHAtq4.jpg?raw=true'],
                7:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/dark_LiuSxa2pyHI.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/drama_T6UiaO8W64k.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/melancholic_A7Ez7OcJYUI.jpg?raw=true', ##advertisement
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/dark_6scwbydd-Uo.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/dark_PxIMp_N-yiM.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/melancholic_2Fqp9NVG2Hg.jpg?raw=true'],
                8:['https://github.com/ppjjee/MuFiB/blob/main/sim_images/happy_Esgna_yA02Y.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/sad_Fs_RNpOMmF8.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/dark_FwxhoQzfUm4.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/commercial_-FH4jY1xmyc.jpg?raw=true', ##funny
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/commercial_v8PPgZHAtq4.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/film_L7f0FGba-60.jpg?raw=true',
                'https://github.com/ppjjee/MuFiB/blob/main/sim_images/retro_HvchVUG3KYw.jpg?raw=true'],
                }

                ###################################################
                ## 함수로 만들기!!!!
                cols = st.columns(10)
                def tag_selector (sim_images, clicked_images):
                    for k, v in sim_images.items():
                        if clicked_images == k:
                            for i in range(len(sim_images[clicked_images])):
                                try:
                                    cols[i].markdown(f'Image #'+str(i+1))
                                    cols[i].image(v[i], use_column_width=True)
                                except IndexError:
                                    pass
                                continue
                            else:
                                print(clicked_images)

                    length = len(sim_images[clicked_images])
                    return length
                
                length = tag_selector(similar_images3, clicked)
                ## 함수 콜백
                # if st.session_state.active_page == 'Page_1':
                #     length = tag_selector(similar_images, clicked)
                # elif st.session_state.active_page == 'Page_3':
                #     length = tag_selector(similar_images2, clicked)
                # elif st.session_state.active_page == 'Page_5':
                #     length = tag_selector(similar_images3, clicked)

                options = st.multiselect(
                    'Add images that expresses similar mood or situation. If there is no similar image, or if you want to search music directly without selecting a similar image, please click the next button below.',
                    list(range(1, length+1))
                )
                print('Added image numbers are:', options)
                

                def adding_tags(sim_images, clicked_images, options):
                    added_tags = []
                    for i in options:
                        a = sim_images[clicked_images][i-1] #1부터 받기 때문에 실제로는 -1을 해주어야 list 값과 일치함
                        b = a.split('/')[-1]
                        c = b.split('_')[0]
                        added_tags.append(c)
                    print('added tags are:', added_tags)
                    return added_tags
                
                added_tags = adding_tags(similar_images3, clicked, options)
                ## 함수 콜백
                # if st.session_state.active_page == 'Page_1':
                #     added_tags = adding_tags(similar_images, clicked, options)
                # elif st.session_state.active_page == 'Page_3':
                #     added_tags = adding_tags(similar_images2, clicked, options)
                # elif st.session_state.active_page == 'Page_5':
                #     added_tags = adding_tags(similar_images3, clicked, options)

                ####################################################
                aggregated_tags= list(set(selected_tags) | set(added_tags))
                if '-' in aggregated_tags:
                    aggregated_tags.remove('-')
                else:
                    pass
                print('mood/theme aggregated tags are:', aggregated_tags)

                genre_tags = {'background':'easylistening','film':'soundtrack', 'melancholic':'ambient', 'children': 'soundtrack', 'relaxing': 'classical',
                'meditative': 'classical', 'cool': 'electronic', 'emotional': 'classical', 'documentary': 'soundtrack', 'love': 'pop', 
                'drama': 'soundtrack', 'adventure': 'orchestral', 'heavy': 'metal', 'dark': 'ambient', 'retro': 'pop', 'ballad': 'pop',
                'epic': 'classical', 'calm': 'classical', 'slow': 'experimental', 'energetic':'electronic', 'deep': 'house', 'inspiring':'easylistening',
                'soft': 'easylistening', 'space': 'electronic', 'fun': 'pop', 'horror': 'soundtrack', 'positive':'pop', 'happy':'pop', 'summer':'chillout',
                'dream':'ambient', 'romantic':'easylistening', 'sad':'classical', 'hopeful':'easylistening', 'motivational':'pop', 
                'uplifting': 'pop', 'party':'dance','mellow':'chillout', 'groovy':'pop', 'soundscape':'ambient', 'corporate':'pop', 
                'advertising':'soundtrack','sport':'rock', 'sexy':'lounge', 'fast':'electronic', 'nature':'ambient', 'commercial':'pop', 
                'funny':'dance','dramatic':'orchestral', 'holiday':'pop', 'ambiental':'soundtrack', 'christmas':'pop', 'game':'electronic', 
                'travel':'pop','powerful':'rock', 'upbeat':'hiphop', 'movie':'soundtrack', 'action':'rock', 'trailer':'trailer'}
                    
                keywords_associated_genre = []
                for i in aggregated_tags:
                    for k, v in genre_tags.items():
                        if i in k:
                            keywords_associated_genre.append(v)
                        else:
                            pass
                print('The keyword related to the genre are:', keywords_associated_genre)

                final_aggregated_tags= list(set(aggregated_tags) | set(keywords_associated_genre))
                print('Final aggregated tags are:', final_aggregated_tags)

                st.experimental_set_query_params(path=save_path)
                st.button('NEXT', on_click=cb, args=(save_path, scenario, clicked, selected_tags, added_tags, options, final_aggregated_tags, ))


            else:
                model_load_state.info(f"**There is no image selected. Please select a sample image.**")
                
        except Exception as e:
            print("Oops!", e.__class__, "occurred.")
            print(e)
            message_container = st.empty() 
            message = message_container.write('👉 Please, wait. We are working on it...! 👀')
            if message != '':
                message_container.empty()

## ------------------ for Mood Music Retrieval ------------------------    
def TagLoad(path):
    f = open(path)
    data = json.load(f)
    tags = data['submits'][-1]['Final aggregated tags']  #tags = ['sad', 'calm', 'emotional']
    print('tags are', tags)
    music_tag = list(tags)
    return music_tag


mood_theme_list = ['background', 'film', 'melancholic', 'calm', 'melodic', 'children', 'relaxing', 'meditative', 'cool', 'documentary', 'emotional', 'space', 'love', 'drama', 
'adventure', 'heavy', 'dark', 'soft', 'energetic', 'retro', 'ballad', 'advertising', 'epic', 'action', 'dramatic', 'powerful', 'upbeat', 'inspiring', 'uplifting', 'soundscape', 'slow', 
'deep', 'fun', 'horror', 'nature', 'funny', 'happy', 'positive', 'summer', 'dream', 'romantic', 'sad', 'hopeful', 'mellow', 'motivational', 'party', 'groovy', 'corporate', 'sport', 'travel', 
'sexy', 'movie', 'fast', 'commercial', 'holiday', 'ambiental', 'christmas', 'game', 'trailer']

def music_retrieval():
    # remoteFilePath = '/nas2/epark/mtg-jamendo-dataset/data/autotagging_moodtheme.tsv'
    remoteFilePath = '/nas3/epark/workspace/IMR/autotagging_moodthemegenre.tsv' 
    localFilePath = 'autotagging_moodthemegenre.tsv'
    sftp.download(remoteFilePath, localFilePath)
    tracks, tags, extra = commons.read_file(localFilePath)

    find_tag_list = []
    save_path = st.experimental_get_query_params()['path'][0]
    print("save path: " + save_path)
    music_tag = TagLoad(save_path)
    for i in music_tag:
        if i in mood_theme_list:
            p = tags['mood/theme'][i]
            q = list(p)
            find_tag_list.extend(q)
            # print('length of find_tag_list', len(find_tag_list))
        else:
            p = tags['genre'][i]
            q = list(p)
            find_tag_list.extend(q)
    print('length of find_tag_list', len(find_tag_list))
 
    
    newlist = [] # empty list to hold unique elements from the list
    duplist = [] # empty list to hold the duplicate elements from the list
    for i in find_tag_list:
        if i not in newlist:
            newlist.append(i)
        else:
            duplist.append(i) # this method catches the first duplicate entries, and appends them to the list
    print('length of duplicated music:', len(duplist)) 
    
    if len(duplist) > 5:
        random_all = random.choices(duplist, k=5)
        st.session_state['music_random'] = random_all
        for r in random_all:
            print(r) # for debug 
    else:
        random_all = random.choices(duplist, k=len(duplist))
        st.session_state['music_random'] = random_all
        for r in random_all:
            print(r) # for debug 
        

    
def createAudio(filename):
    remoteFilePath = sftp.dirRemoteMusicData + '/' + filename
    localFilePath = sftp.dirMusic + '/' + filename
    sftp.download(remoteFilePath, localFilePath)
    audio_file = open(localFilePath, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg', start_time=0)

## streamlit display codes
def music_page(cb):
    st.title('Music Finder 🎵')
    st.subheader("Now, we find music lists that match the image!")
    st.caption('- The music searched in this study is a copyright-free sound sources provided for research purposes.')
    st.caption('- Therefore, we inform you that it may be different from the latest music you are familiar with.')
    st.write('-----')
    st.markdown("🎧 Please enjoy the music and answer the questions below. 🎧")
    st.caption("- Listen to music for at least 30 seconds and answer the question (slide bar) below.")
    st.markdown(hide_menu, unsafe_allow_html = True)

    random_all = st.session_state['music_random']
    for r in random_all:
        print(r) # for debug
        createAudio(str(r) + '.mp3')

    st.write('-----')

    ## save results
    with st.container():
        # satis_result = st.slider('Do you think the retrieved music represents the selected image well?', min_value=0, max_value=100, value=50, step=1)
        satis_result = st.select_slider('Overall, do you think the retrieved music matches the selected images well?', options=['Strongly disagree', 'Disagree', 'Somewhat disagree', 'Neither agree nor disagree', 'Somewhat agree', 'Agree', 'Strongly agree'], value='Neither agree nor disagree')
        st.caption("- Note: Please evaluate how well the selected image represents the music, rather than providing a 'like' or 'dislike' rating for the provided music.")
        st.write('-----')
    
        save_path = st.experimental_get_query_params()['path'][0]
        with open(save_path, "r") as json_file:
            results_B = {'Music Satisfaction': satis_result}
            data = json.load(json_file)
            data['submits'][-1].update(results_B)

        with open(save_path, "w") as save_f:
            json.dump(data, save_f, ensure_ascii=False, indent=4)    
            print("exists, after", data)
        
        st.experimental_set_query_params(path=save_path)
        st.button('NEXT', on_click=cb, args=(save_path, satis_result))


## ------------------ for Survey ------------------------ 
def survey_page():
    save_path = st.experimental_get_query_params()['path'][0]
    print("path 5: " + save_path)
    st.title('Final survey')
    st.markdown("**This is the last step. Please answer the questions below.**")
    st.markdown("<span style='color:red'>An insincere response will be regarded as abandoning the experiment.  Please provide sincere responses until the end.</span>",unsafe_allow_html=True)
    st.caption("💪 You are almost there!")
    st.markdown(hide_menu, unsafe_allow_html = True)

    survey = st.container()
    with survey:
        st.write('-----')
        
        gender = st.radio(
            "What's your gender?",
            ('Male', 'Female', 'Non-binary/Third gender'))

        age = st.radio(
            "What's your age range?",
            ('20s', '30s', '40s', '50s', '60s', 'Above 60s'))

        education = st.radio(
            "What's the highest level of education that you have completed?",
            ('Less than high school', 'High school graduate', 'Some college', '2 year degree', '4 year degree', 'Professional degree', 'Doctorate'))
            # ('Primary/Elementary education not completed', 'Primary/Elementary education', 'Secondary education','Further education (Bachelor degree, diploma', 'Higher education (Masters, Doctorate)'))

        ethnicity = st.radio(
            "What's your ethnicity (or race)?",
            ('Prefer not to disclose', 'American Indigenous (Alaskan Native / Native American)', 'Asian', 'Black', 'Latinx / Hispanic', 'Middle Eastern / North African', 'Pacific Islander', 'White / Caucasian', 'Multi Race / Ethnicity'))

        service = st.text_input(
            "What service do you use to search for music? (Example: Spotify, YouTube Music)")

        if not service:
            st.warning("Please kindly provide a response to the question.")

        inconvenient = st.text_input(
            "What was the most inconvenient thing about searching for music using the music search service you answered above?")
        
        if not inconvenient:
            st.warning("Please kindly provide a response to the question.")
        st.write('-----')

        sus1 = st.radio(
            "Overall, I am satisfied with how easy it is to use this system.",
            ('Strongly Agree', 'Agree', 'Somewhat Agree', 'Niether Agree Nor Disagree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree'))

        sus2 = st.radio(
            "It was simple to use this system.",
            ('Strongly Agree', 'Agree', 'Somewhat Agree', 'Niether Agree Nor Disagree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree'))
        
        sus3 = st.radio(
            "I was able to complete the tasks and scenarios quickly using this system.",
            ('Strongly Agree', 'Agree', 'Somewhat Agree', 'Niether Agree Nor Disagree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree'))

        sus4 = st.radio(
            "I felt comfortable using this system.",
            ('Strongly Agree', 'Agree', 'Somewhat Agree', 'Niether Agree Nor Disagree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree'))

        sus5 = st.radio(
            "It was easy to learn to use this system.",
            ('Strongly Agree', 'Agree', 'Somewhat Agree', 'Niether Agree Nor Disagree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree'))
        
        sus6 = st.radio(
            "I believe I could become productive quickly using this system.",
            ('Strongly Agree', 'Agree', 'Somewhat Agree', 'Niether Agree Nor Disagree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree'))

        sus7 = st.radio(
            "The system gave error messages that clearly told me how to fix problems.",
            ('Strongly Agree', 'Agree', 'Somewhat Agree', 'Niether Agree Nor Disagree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree'))

        sus8 = st.radio(
            "Whenever I made a mistake using the system, I could recover easily and quickly.",
            ('Strongly Agree', 'Agree', 'Somewhat Agree', 'Niether Agree Nor Disagree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree'))

        sus9 = st.radio(
            "The information provided with this system was clear.",
            ('Strongly Agree', 'Agree', 'Somewhat Agree', 'Niether Agree Nor Disagree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree'))

        sus10 = st.radio(
            "It was easy to find the information I needed.",
            ('Strongly Agree', 'Agree', 'Somewhat Agree', 'Niether Agree Nor Disagree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree'))

        sus11 = st.radio(
            "The information was effective in helping me complete the tasks and scenarios.",
            ('Strongly Agree', 'Agree', 'Somewhat Agree', 'Niether Agree Nor Disagree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree'))

        sus12 = st.radio(
            "The organization of information on the system screens was clear.",
            ('Strongly Agree', 'Agree', 'Somewhat Agree', 'Niether Agree Nor Disagree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree'))

        sus13 = st.radio(
            "The interface of this system was pleasant.",
            ('Strongly Agree', 'Agree', 'Somewhat Agree', 'Niether Agree Nor Disagree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree'))

        sus14 = st.radio(
            "I liked using the interface of this system.",
            ('Strongly Agree', 'Agree', 'Somewhat Agree', 'Niether Agree Nor Disagree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree'))

        sus15 = st.radio(
            "This system has all the functions and capabilities I expect it to have.",
            ('Strongly Agree', 'Agree', 'Somewhat Agree', 'Niether Agree Nor Disagree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree'))

        sus16 = st.radio(
            "Overall, I am satisfied with this system.",
            ('Strongly Agree', 'Agree', 'Somewhat Agree', 'Niether Agree Nor Disagree', 'Somewhat Disagree', 'Disagree', 'Strongly Disagree'))

        situation = st.text_input(
            "If this system becomes commercially available, in what situations do you think you will use it? (Example: When I want to listen to new music, but it is difficult to express my search terms in text.)")

        if not situation:
            st.warning("Please kindly provide a response to the question.")

        improved = st.text_input(
            "What aspects of the system you have used would you like to see improved?")

        if not improved:
            st.warning("Please kindly provide a response to the question.")
        st.write('-----')

        st.markdown('Please read the question and choices carefully before providing your answer.')
        
        ux1 = st.select_slider('Was the system obstructive or supportive?',options=['Obstructive: 0', 1, 2, 3, 4, 5, 6, 'Supportive: 7'], value=4)
        
        ux2 = st.select_slider('Was the system complicated or easy?',options=['Complicated: 0', 1, 2, 3, 4, 5, 6, 'Easy: 7'], value=4)
        
        ux3 = st.select_slider('Was the system inefficient or efficient?',options=['Inefficient: 0', 1, 2, 3, 4, 5, 6, 'Efficient: 7'], value=4)

        ux4 = st.select_slider('Was the system confusing or clear?',options=['Confusing: 0', 1, 2, 3, 4, 5, 6, 'Clear: 7'], value=4)

        ux5 = st.select_slider('Was the system boring or exciting?',options=['Boring: 0', 1, 2, 3, 4, 5, 6, 'Exciting: 7'], value=4)

        ux6 = st.select_slider('Was the system not interesting or interesting?',options=['Not interesting: 0', 1, 2, 3, 4, 5, 6, 'Interesting: 7'], value=4)

        ux7 = st.select_slider('Was the system conventional or inventive?',options=['Conventional: 0', 1, 2, 3, 4, 5, 6, 'Inventive: 7'], value=4)

        ux8 = st.select_slider('Was the system usual or leading edge?',options=['Usual: 0', 1, 2, 3, 4, 5, 6, 'Leading edge: 7'], value=4)

        
        
        # ux1 = st.select_slider('Did the system usage experience annoying you or was it enjoyable?', options=['Annoying: 0', 1, 2, 3, 4, 5, 6, 'Enjoyable: 7'], value=4)
 
        # ux2 = st.select_slider('Did you have trouble understanding how to use the system?',options=['Not understandable: 0', 1, 2, 3, 4, 5, 6, 'Understandable: 7'], value=4)

        # ux3 = st.select_slider('Was the system creative or dull?',options=['Creative: 0', 1, 2, 3, 4, 5, 6, 'Dull: 7'], value=4)
        
        # ux4 = st.select_slider('Was it easy or difficult to learn how to use the system?',options=['Easy to learn: 0', 1, 2, 3, 4, 5, 6, 'Difficult to learn: 7'], value=4)
        
        # ux5 = st.select_slider('Was the system valuable or inferior?',options=['Valuable: 0', 1, 2, 3, 4, 5, 6, 'Inferior: 7'], value=4)

        # ux6 = st.select_slider('Was the system boring or exciting?',options=['Boring: 0', 1, 2, 3, 4, 5, 6, 'Exciting: 7'], value=4)

        # ux7 = st.select_slider('Was the system not interesting or interesting?',options=['Not interesting: 0', 1, 2, 3, 4, 5, 6, 'Interesting: 7'], value=4)

        # ux8 = st.select_slider('Was the system unpredictable or predictable?',options=['Unpredictable: 0', 1, 2, 3, 4, 5, 6, 'Predictable: 7'], value=4)

        # ux9 = st.select_slider('Was the system fast or slow?',options=['Fast: 0', 1, 2, 3, 4, 5, 6, 'Slow: 7'], value=4)

        # ux10 = st.select_slider('Was the system inventive or conventional?',options=['Inventive: 0', 1, 2, 3, 4, 5, 6, 'Convnentional: 7'], value=4)

        # ux11 = st.select_slider('Was the system obstructive or supportive?',options=['Obstructive: 0', 1, 2, 3, 4, 5, 6, 'Supportive: 7'], value=4)

        # ux12 = st.select_slider('Was the system good or bad?',options=['Good: 0', 1, 2, 3, 4, 5, 6, 'Bad: 7'], value=4)

        # ux13 = st.select_slider('Was the system complicated or easy?',options=['Complicated: 0', 1, 2, 3, 4, 5, 6, 'Easy: 7'], value=4)

        # ux14 = st.select_slider('Did the system usage experience unlikable or was it pleasing?',options=['Unlikable: 0', 1, 2, 3, 4, 5, 6, 'Pleasing: 7'], value=4)

        # ux15 = st.select_slider('Was the system usual or leading edge?',options=['Usual: 0', 1, 2, 3, 4, 5, 6, 'Leading edge: 7'], value=4)

        # ux16 = st.select_slider('Did the system usage experience unpleasant or was it pleasant?',options=['Unpleasant: 0', 1, 2, 3, 4, 5, 6, 'Pleasant: 7'], value=4)

        # ux17 = st.select_slider('Was the system secure or not secure?',options=['Secure: 0', 1, 2, 3, 4, 5, 6, 'Not secure: 7'], value=4)

        # ux18 = st.select_slider('Was the experience of using the system motivating or demotivating?',options=['Motivating: 0', 1, 2, 3, 4, 5, 6, 'Demotivating: 7'], value=4)

        # ux19 = st.select_slider('Did the system usage experience meet your expectations or did it not meet your expectations?',options=['Meets expectations: 0', 1, 2, 3, 4, 5, 6, 'Does not meet expectations: 7'], value=4)

        # ux20 = st.select_slider('Was the system inefficient or efficient?',options=['Inefficient: 0', 1, 2, 3, 4, 5, 6, 'Efficient: 7'], value=4)

        # ux21 = st.select_slider('Was the system clear or confusing?',options=['Clear: 0', 1, 2, 3, 4, 5, 6, 'Confusing: 7'], value=4)

        # ux22 = st.select_slider('Was the system impractical or practical?',options=['Impractical: 0', 1, 2, 3, 4, 5, 6, 'Practical: 7'], value=4)

        # ux23 = st.select_slider('Was the system organized or cluttered?',options=['Organized: 0', 1, 2, 3, 4, 5, 6, 'Cluttered: 7'], value=4)

        # ux24 = st.select_slider('Was the system attractive or unattractive?',options=['Attractive: 0', 1, 2, 3, 4, 5, 6, 'Unattractive: 7'], value=4)

        # ux25 = st.select_slider('Was the system friendly or unfriendly?',options=['Friendly: 0', 1, 2, 3, 4, 5, 6, 'Unfriendly: 7'], value=4)

        # ux26 = st.select_slider('Was the system conservative or innovative?',options=['Conservative: 0', 1, 2, 3, 4, 5, 6, 'Innovative: 7'], value=4)


        id = st.session_state['id']
        st.text(f"Here is your ID: " + id)
        st.text('Copy this value to paste into MTurk.')
        st.text('When you have copied this ID, please click the check box below to submit your survey.')

        ## save results
        if st.checkbox("Do you want to move to the next page?", key='fin'):
            results_B = {'gender': gender, 'age': age, 'education': education, 'ethnicity': ethnicity,
             'service':service, 'inconvenient':inconvenient, 'sus1': sus1, 'sus2': sus2, 'sus3': sus3, 
             'sus4': sus4, 'sus5': sus5, 'sus6': sus6, 'sus7': sus7, 'sus8': sus8,'sus9': sus9,
             'sus10': sus10, 'sus11': sus11, 'sus12': sus12, 'sus13': sus13, 'sus14': sus14, 'sus15': sus15,
             'sus16': sus16, 'situation': situation, 'improved': improved,
             'ux1': ux1, 'ux2': ux2, 'ux3': ux3, 'ux4': ux4, 'ux5': ux5, 'ux6': ux6, 
             'ux7': ux7, 'ux8': ux8, 'workerID' : id
             }
            with open(save_path, "r") as json_file:
                data = {}
                data = json.load(json_file)
            data['submits'].append(results_B)

            with open(save_path, "w") as save_f:
                json.dump(data, save_f, ensure_ascii=False, indent=4)
                print("exists, after", data)
            
            id = st.session_state['id']
            sftp.upload(save_path, sftp.dirRemoteSurveyResult + '/' + id + ".json")
            st.button('END', on_click=CB_Page9)  
                                                

## ------------------ for Final ------------------------ 
def final_page():
    st.balloons()
    st.title("Thank you for your participation!")
    st.markdown(hide_menu, unsafe_allow_html = True)       


# run the active page
if st.session_state.active_page == 'Home':
    home()
# elif st.session_state.active_page == 'Page_0':
#     note()
elif st.session_state.active_page == 'Page_1':
    image_page1(mood_imgs, CB_Page1)
elif st.session_state.active_page == 'Page_2':
    music_page(CB_Page2)
elif st.session_state.active_page == 'Page_3':
    image_page2(mood_imgs2, CB_Page3)
elif st.session_state.active_page == 'Page_4':
    music_page(CB_Page4)
elif st.session_state.active_page == 'Page_5':
    image_page3(theme_imgs, CB_Page5)
elif st.session_state.active_page == 'Page_6':
    music_page(CB_Page6)
# elif st.session_state.active_page == 'Page_7':
#     image_page(theme_imgs2, CB_Page7)
# elif st.session_state.active_page == 'Page_8':
#     music_page(CB_Page8)
elif st.session_state.active_page == 'Page_9':
    survey_page()
elif st.session_state.active_page == 'Page_10':
    final_page()
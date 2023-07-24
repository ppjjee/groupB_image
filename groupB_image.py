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
    

def save_image_tag_result(save_path, scenario, clicked, selected_tags, added_tags, final_aggregated_tags):
    # conv_change = []
    # for i, c in enumerate(change):
    #     target = c
    #     if c == "-":
    #         target = selected_tags[i]
    #     conv_change.append(target)
    # print(conv_change)
    results_B = {'Scenario': scenario, 'Image': f"{str(int(clicked)+1)}", 'Selected image tags': selected_tags, 'Added tags': added_tags, 'Final aggregated tags': final_aggregated_tags}
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

# callback functions for change page
def CB_Home():
    st.session_state.active_page = 'Page_1'

# def CB_Page0():
#     st.session_state.active_page = 'Page_1'

def CB_Page1(save_path, scenario, clicked, selected_tags, added_tags, final_aggregated_tags):
    save_image_tag_result(save_path, scenario, clicked, selected_tags, added_tags, final_aggregated_tags)
    music_retrieval()
    st.session_state.active_page = 'Page_2'

def CB_Page2():
    st.session_state.active_page = 'Page_3'

def CB_Page3(save_path, scenario, clicked, selected_tags, added_tags, final_aggregated_tags):
    save_image_tag_result(save_path, scenario, clicked, selected_tags, added_tags, final_aggregated_tags)
    music_retrieval()
    st.session_state.active_page = 'Page_4'

def CB_Page4():
    st.session_state.active_page = 'Page_5'

def CB_Page5(save_path, scenario, clicked, selected_tags, added_tags, final_aggregated_tags):
    save_image_tag_result(save_path, scenario, clicked, selected_tags, added_tags, final_aggregated_tags)
    music_retrieval()
    st.session_state.active_page = 'Page_6'

def CB_Page6():
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
                'https://github.com/ppjjee/MuFiB/blob/main/images/relaxing.jpg?raw=true', # 1번째로 이동      
                'https://github.com/ppjjee/MuFiB/blob/main/images/travel.jpg?raw=true', # 1번째로 이동
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
                'https://github.com/ppjjee/MuFiB/blob/main/images/melodic.jpg?raw=true',
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
    ('Feeling tired but unable to sleep: Search for music to listen to in such a situation.', 
    'During exercise (yoga or fitness, etc.): Search for music to listen to in such a situation.', 
    'Preparing for a party: Search for music to listen to in such a situation.'))
    st.markdown("✔️ STEP 2: Click on the image that best represents your selected scenario. After selecting an image, please wait for a while until the next process.")
    
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
                similar_images = {0:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/dark_rSfuFUb-zD8.jpg', # /nas3/epark/workspace/retreival/unsplash_data_merge_new/dark_rSfuFUb-zD8.jpg
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/summer_m-3BcC8xSWo.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/adventure_UiEPEzSwf5Y.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/fast_OnmDVnyofVM.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/summer_vSfefVjrGz4.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/action_IQdMxDnhuzI.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/adventure_q9rpNOd1hcI.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/film_aCX-pyyczyE.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/adventure_2G4XSjqzMyk.jpg'], 
                1:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/dramatic_M1o0YeTvb0w.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_o364nYBlfvI.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/sad_rVxwmum9Rjs.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/drama_JWZHw_FXxFM.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/dark_xd9ki66m_AA.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/emotional_sO6yji4O_FI.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_werrs0UfZvU.jpg'], 
                2:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/melodic_DXHog7Ktrwg.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/retro_zKaTW0Jv4jM.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/energetic_31HS1aQ1tMw.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_t-j4MkVyqFQ.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/melodic_8fbXv0PW6qk.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/melodic_P1NCcANxyYQ.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/corporate__ssmNHkymiA.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/melodic_Visxcphdymk.jpg'], 
                3:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/love_-1qIRIqN14A.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/love_E8FaHPExFNg.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/melodic_3hiVgZkxr7g.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/background_SQ1kv2upHbc.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/background_Z1A2U0vo8uY.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/background_XL5ysBNBV5I.jpg'], 
                4:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_0214ke7k2dI.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/groovy_4XJcFMeBoZc.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/meditative_1GrlsYupLP8.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_IwI0g4ef9cQ.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_QEZOlAZXWq0.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_zdShIOOI3_4.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_QmTeMHweRp8.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_kUqJ5Kf14JA.jpg'],
                5:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/party_VBsG1VOgLIU.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/game_Yl7Y8DhyzyY.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/holiday_Cf-iAhAiqwo.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/cool_VUKlc1KDLwo.jpg', 
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/soft_63IDHmoQpL0.jpg', 
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/party_W9GvbwOd120.jpg', 
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/party_zYfFGI3Xw7M.jpg', ##children
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/romantic__afBES698bA.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/holiday_Qf17ez87hLg.jpg'],
                6:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_Ve3hWAANHSU.jpg', 
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/relaxing_OZiflZqq0N0.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/relaxing_FYaaWYcbPOY.jpg', ##retro
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/relaxing_4Wlp6m8hroE.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/relaxing_0Ymt53tBapQ.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/relaxing_4DxjAJxXE7c.jpg'],
                7:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/adventure_JHxBeZfIsck.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/travel_dvl4C_4S9Q0.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/cool_VLWuCo6H7h8.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/travel_qrjCpGh5td0.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/travel_RPcIkOzN0iQ.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/travel_LrvqwqEzxa4.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/travel_S9ts_A3-khk.jpg',##children
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/travel_hArsf0-tVj8.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/funny_foPx39kj7Rw.jpg'],
                8:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/party_GIXpWit5kY0.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/happy_FgHvCcj3Jus.jpg', ##dark
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/party_eyFGaU4vKog.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/party_Wm-GDBlJU8k.jpg', ##movie
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/party_hl0yBiB4i5M.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/happy_rnNFHYzz0Ww.jpg', ##christmas
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/party_Ie_dMMsT_Ww.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/christmas_VlXBwLZ_L94.jpg'],
                9:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/holiday_z2esruz6gtU.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/summer_c29cb9moISE.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/groovy_U_pZityO2oo.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/retro_JS3aOzdzBsI.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/holiday_xAHfhMcsAc8.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/party_ZFBx9mWbYQs.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/party_5JtuW6PqGKE.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/holiday_hiG9H-qybaw.jpg'],
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
                st.button('NEXT', on_click=cb, args=(save_path, scenario, clicked, selected_tags, added_tags, final_aggregated_tags, ))


            else:
                model_load_state.info(f"**Please select a preferred scenario fist, and click on the image that best represents the scenario.**")
                
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
    ('Want to discover a new music: Search for music to listen to in such a situation.', 
    'Playing with a child: Search for music to listen to in such a situation.', 
    'Studying or working: Search for music to listen to in such a situation.'))
    st.markdown("✔️ STEP 2: Click on the image that best represents your selected scenario. After selecting an image, please wait for a while until the next process.")
    
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
                similar_images2 = {0:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/melodic_S0oqXncDqP8.jpg', ## action
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/dream_CetnsEMUydc.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/cool_4zXx50JLTnY.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/positive_JQXe2vrbNOA.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/film_j4cOKZojvNI.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/soft_fsbfVrhpV6k.jpg', ##christmas
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/happy_ewH71a1zdmA.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/soft_jGVySnyIPXc.jpg'], 
                1:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/love_ZshVGzJ6a_s.jpg', ##cool
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/cool_WtFvRYuS7wc.jpg', ##adventure
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/motivational_Oy2DiS1XXGc.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/love_XLFKpzK8m_Q.jpg', 
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/motivational_TpaWqZrSP1o.jpg'], ##sport
                2:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/nature_qJmfb_wWXhw.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/nature_60XLoOgwkfA.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/sad_p_-bbbzy87s.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/sad_exI3uXWZgwo.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_KhPtWXmV-cY.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/film__o2kocC8kiY.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/background_XfG2S7ca7hI.jpg'],
                3:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/happy_rxB0L6nrP5M.jpg', # children_game
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/game_eLZJTFPCfA8.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/children_Un8NnnQOMfA.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/children_3BztcJxliEM.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/funny_Uz5nEXMceSk.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/fun_04-RGWREZaU.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/game_LjAAUZadNrg.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/game_FEhFnQdLYyM.jpg'],
                4:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/corporate_s6w5NOxtm7U.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/corporate_a7A9O5htrKs.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new/corporate___DIXb69qyY.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new/corporate_CPs2X8JYmS8.jpg',],
                5:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/children_ZSsJBGhor6I.jpg', #children
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/happy_3ShDt858xes.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/party_phm8rn2thkk.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/fun_F8G44Qm_lCA.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/fun_buN4aX5JaNs.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/children_FCxZ0hDm4FA.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/children_dtSm9l9GlHE.jpg'],
                6:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/retro_yZVBebc1GnE.jpg', # retro_motivational
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_6URZVbb7r-c.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_DjJ49s6uD2o.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/motivational_B4Ngz_pdvz4.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_XNwy-SuaH4M.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/meditative_AigO5TWibjk.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/meditative_4Gi3H-4evlk.jpg'],
                7:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/dark_nn9qPOjPNag.jpg', #nature_dark
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/nature_ZBi4YhdiyPo.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/trailer_Rv9j87zTc_E.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/nature_qOktg322Byw.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/dark_w-lINiHiH64.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/deep_Q6tmUuUSCkc.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/deep_--kGuWTwn48.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_yxJs9n5W3Ns.jpg'],
                8:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/melancholic_Q0yUoNhAR04.jpg', #trailer_melancholic
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/dark_yF9yF94sLoM.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/dark_Qs5cp4NARUQ.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/dark_cnAmaEgSRsU.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/melancholic_H8dDVFCqeKA.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/background_4kYCGOyMsiQ.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/melancholic_eow7_24T-gU.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/dark_0cZj4pz1VW0.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_JgiYHgWU0Do.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/dark_nkXDGnqFb7g.jpg'],
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
                st.button('NEXT', on_click=cb, args=(save_path, scenario, clicked, selected_tags, added_tags, final_aggregated_tags, ))


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
    ('Commuting to and from work: Search for music that matches your current mood in such a situation.', 
    'Driving: Search for music that matches your current mood in such a situation.', 
    'Emotional early morning hours: Search for music that matches your current mood in such a situation.'))
    st.markdown("✔️ STEP 2: Click on the image that best represents your selected scenario. After selecting an image, please wait for a while until the next process.")
    
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
                similar_images3 = {0:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/adventure_9aUQlS6Pgns.jpg', # trailer_adventure_commercial
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/trailer_w8kIQEU34Po.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/energetic_VK2KjAfvOPs.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/trailer_ktltWUbd1lk.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_RKf6vgN12qM.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/commercial_zmBfXGF6Otg.jpg'],
                1:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/relaxing_IgomcyU3PCs.jpg', #relaxing_calm
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/relaxing_VfWYEniF5K8.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm__GAfRnQzXA4.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_Urh0w8Rpwpg.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/relaxing_if6hfEkqFNk.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/calm_aPJif68ghkg.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/love_1xzSAlZUVSc.jpg'],
                2:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/melodic_DiNNWOqplfU.jpg', #melodic
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/melodic_jJGc21mEh8Q.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/melodic_9nQwnympSfw.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/upbeat_OsgLI_awdk0.jpg'], 
                3:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/adventure_h0Af70v6p0o.jpg', #adventure_meditative
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/meditative_eA2t5EvcxU4.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/uplifting_w28Ei0Ap96w.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/sad_gQ3NgmHj5tY.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/adventure_qIzSE8QcXkE.jpg'],
                4:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/melodic_Z-4RFLosaMs.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/adventure_FlFHP9kNeuE.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/melodic_bxq2uYtDCLk.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/happy_qScXkp4uBXU.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/adventure_qymfP660rCI.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/film_nyFSRz02-mQ.jpg'],
                5:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/nature_jwTvCQQJXh0.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/dark_gnLlGA1D8oI.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/nature_pNnUJEN2zns.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/nature_Z6IKZFJA2wQ.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/nature_xY_6ZENqcfo.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/nature_c5IvumengsE.jpg'],
                6:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/film_ZHgOc2qss3U.jpg', 
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/trailer_bmZljCM1ue8.jpg', 
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/holiday_Jojw4XIOmVI.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/adventure_0SURIr_updA.jpg', 
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/trailer_z7pUqeJNWww.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/commercial_v8PPgZHAtq4.jpg'],
                7:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/dark_LiuSxa2pyHI.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/drama_T6UiaO8W64k.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/melancholic_A7Ez7OcJYUI.jpg', ##advertisement
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/dark_6scwbydd-Uo.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/dark_PxIMp_N-yiM.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/melancholic_2Fqp9NVG2Hg.jpg'],
                8:['/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/happy_Esgna_yA02Y.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/sad_Fs_RNpOMmF8.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/dark_FwxhoQzfUm4.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/commercial_-FH4jY1xmyc.jpg', ##funny
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/commercial_v8PPgZHAtq4.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/film_L7f0FGba-60.jpg',
                '/nas3/epark/workspace/retreival/unsplash_data_merge_new_for_experiment/retro_HvchVUG3KYw.jpg'],
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
                st.button('NEXT', on_click=cb, args=(save_path, scenario, clicked, selected_tags, added_tags, final_aggregated_tags, ))


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

    random_all = random.choices(duplist, k=5)
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
        st.button('NEXT', on_click=cb)


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
            "I think that I would like to use this system frequently.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        sus2 = st.radio(
            "I found the system unnecessarily complex.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))
        
        sus3 = st.radio(
            "I thought that the system was easy to use.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        sus4 = st.radio(
            "I think that I would need the support of a technical person to be able to use this system.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        sus5 = st.radio(
            "I found the various functions in this system were well integrated.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))
        
        sus6 = st.radio(
            "I thought there was too much inconsistency in this system.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        sus7 = st.radio(
            "I would imagine that most people would learn to use this system very quickly.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        sus8 = st.radio(
            "I found the system very cumbersome to use.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        sus9 = st.radio(
            "I felt vey confident using the system.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        sus10 = st.radio(
            "I needed to learn a lot of things before I could get going with this system.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))
        
        situation = st.text_input(
            "If this system becomes commercially available, in what situations do you think you will use it? (Example: When I want to listen to new music, but it is difficult to express my search terms in text.")

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
             'sus10': sus10, 'situation': situation, 'improved': improved,
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
elif st.session_state.active_page == 'Page_0':
    note()
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
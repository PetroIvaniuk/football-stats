import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st

# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

def get_bar_data_mean(df, value_column, label_column):
    df_ = df.copy()
    df_['Mean_{}'.format(value_column)] = (df_[value_column]/df_['#Games']).apply(lambda x: round(x, 2))
    df_ = df_.sort_values('Mean_{}'.format(value_column))
    value_list = df_['Mean_{}'.format(value_column)].to_list()
    label_list = df_[label_column].to_list()
    return value_list, label_list

def plot_bar_h(value_list, label_list):
    fig = plt.figure(figsize=(6, 10), dpi=100)
    ax = fig.add_subplot()
    bar_width = 0.8
    ax.barh(y=label_list, width=value_list, height=bar_width, color=['#009A17'])
    offset = min(value_list)*0.1
    for patch in ax.patches:
        ax.text(patch.get_width() + offset,
                patch.get_y()+patch.get_height()/2,
                patch.get_width() if patch.get_height()!=0 else '', 
                va="center", fontsize=12)
    ax.tick_params(labelbottom=False, bottom=False, labelsize=14)
    ax.spines['bottom'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    st.pyplot(plt)

def main():
    pages = {
        "Ліга": page_first,
        "Команди": page_second,
        "Гравці": page_third,
        "Судді": page_fourth,
        "Події": page_fifth,
    }

    st.set_page_config(page_title='Football Stats App', layout="wide")
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    _, col01, _ = st.columns((2, 2, 2))
    with col01:
        st.title('Football Statistics App')
        page = st.radio('', tuple(pages.keys()))

    pages[page]()

def page_first():

    select_dict = {
        'кількість голів':'Gls', 
        'кількість ударів':'Sh', 
        'кількість ударів в площину':'SoT', 
        'кількість офсайдів':'Off', 
        'кількість фолів':'Fls'
        }

    df_team = data_players.groupby('Team')[['Gls', 'Sh', 'SoT', 'Captain', 'Att', 'Fls', 'Off', 'OG']]\
                          .sum().rename(columns={'Captain':'#Games'}).reset_index()
    with st.container():
        _, col101, _, col102, _,  = st.columns((0.1, 1, 0.2, 2, 0.1))
        with col101:
            st.write('#### Кількісні Показники')
            metric_selected = st.selectbox('Виберіть покзаник:', select_dict.keys(), key=0)
            st.write('#### Середня {}'.format(metric_selected))
            value_list, label_list = get_bar_data_mean(df_team, select_dict[metric_selected], 'Team')
            plot_bar_h(value_list, label_list)

        with col102:
            st.write('#### Турнірна Таблиця')
            st.table(data_table)

        _, col111, _, col112, _, = st.columns((0.1, 2, 0.2, 2, 0.1))
        with col111:
            st.write('#### Бомбардири')
            df_score = data_players.sort_values('Gls', ascending=False)[['Player', 'Team', 'Pos', 'MP', 'Gls', 'PKatt', 'Ast']][:5].copy()
            df_score = df_score.reset_index(drop=True).rename(columns={'Player':'Гравець', 'Pos':'Позиція', 'Team':'Команда',
                                                                        'MP':'Матчі', 'Gls':'Голи', 'PKatt':'Пенальті', 'Ast':'Асисти'})
            df_score['Голи'] = df_score['Голи'].astype(int)
            df_score['Пенальті'] = df_score['Пенальті'].astype(int)
            df_score['Асисти'] = df_score['Асисти'].astype(int)
            st.table(df_score)

        with col112:
            st.write('#### Асистенти')
            df_ast = data_players.sort_values('Ast', ascending=False)[['Player', 'Team', 'Pos', 'MP', 'Gls', 'PKatt', 'Ast']][:5].copy()
            df_ast = df_ast .reset_index(drop=True).rename(columns={'Player':'Гравець', 'Pos':'Позиція', 'Team':'Команда',
                                                                    'MP':'Матчі', 'Gls':'Голи', 'PKatt':'Пенальті', 'Ast':'Асисти'})
            df_ast['Голи'] = df_ast['Голи'].astype(int)
            df_ast['Пенальті'] = df_ast['Пенальті'].astype(int)
            df_ast['Асисти'] = df_ast['Асисти'].astype(int)
            st.table(df_ast)

        # with col113:
        #     st.write('#### Жовті карточки')
        #     df_cards = data_players.sort_values('CrdY', ascending=False)[['Player', 'Team', 'Pos', 'MP', 'CrdY', 'CrdR',]][:5].copy()
        #     df_cards = df_cards.reset_index(drop=True).rename(columns={'Player':'Гравець', 'Pos':'Позиція', 'Team':'Команда',
        #                                                                'MP':'Матчі', 'CrdY':'Жовті', 'CrdR':'Червоні'})
        #     df_cards['Жовті'] = df_cards['Жовті'].astype(int)
        #     df_cards['Червоні'] = df_cards['Червоні'].astype(int)
        #     st.table(df_cards)

def page_second():
    with st.container():

        team_logo_map = dict(zip(data_logos_img['Team'], data_logos_img['LogoName']))

        _, col201, _, col202, _, = st.columns((0.1, 1, 0.1, 1, 0.1))
        with col201:
            teams_all_2 = data_players['Team'].unique()
            team_selected_1 = st.selectbox('Виберіть команду 1:', teams_all_2, index=6, key=0)
            team_data_1 = data_players[data_players['Team']==team_selected_1].reset_index(drop=True)
            team_data_1['Age'] = team_data_1['Age'].str.split('-').str[0].astype(int)

            # st.table(team_data_1.iloc[:, :8])

        with col202:
            teams_all_2 = data_players['Team'].unique()
            team_selected_2 = st.selectbox('Виберіть команду 2:', teams_all_2, index=5, key=1)
            team_data_2 = data_players[data_players['Team']==team_selected_2].reset_index(drop=True)
            team_data_2['Age'] = team_data_2['Age'].str.split('-').str[0].astype(int)

            # st.table(team_data_2.iloc[:, :8])

        _, col200, _, = st.columns((0.05, 1, 0.05))
        with col200:
            st.write('#### Турнірна Таблиця')
            teams_selected = [team_selected_1, team_selected_2]
            st.table(data_table[data_table['Squad'].isin(teams_selected)])


        df_team = data_players.groupby('Team')[['Gls', 'Sh', 'SoT', 'Captain', 'Att', 'Fls', 'Off', 'OG', 'CrdY', 'CrdR']]\
                              .sum().rename(columns={'Captain':'#Games'}).reset_index()
        df_team_1 = df_team[df_team['Team']==team_selected_1]
        df_team_2 = df_team[df_team['Team']==team_selected_2]

        _, col210, col211, _, col213, col214, _ = st.columns((0.1, 1, 1, 0.1, 1, 1, 0.1))
        with col210:
            st.write('#### {}'.format(team_selected_1))
            st.image(team_logo_map[team_selected_1], width=250)

        with col211:
            st.write('#### ')
            st.write('#### ')
            st.text("Середній Вік Гравців: {}".format(round(team_data_1['Age'].mean(), 2)))
            st.text("Жовті карточки (середнє): {} ({})".format(int(df_team_1['CrdY'].values[0]), 
                                                               round(df_team_1['CrdY'].values[0]/df_team_1['#Games'].values[0], 2)))
            st.text("Червоні карточки (середнє): {} ({})".format(int(df_team_1['CrdR'].values[0]),
                                                            round(df_team_1['CrdR'].values[0]/df_team_1['#Games'].values[0], 2)))

        with col213:
            st.write('#### {}'.format(team_selected_2))
            st.image(team_logo_map[team_selected_2], width=250)

        with col214:
            st.write('#### ')
            st.write('#### ')
            st.text("Середній Вік Гравців: {}".format(round(team_data_2['Age'].mean(), 2)))
            st.text("Жовті карточки (середнє): {} ({})".format(int(df_team_2['CrdY'].values[0]), 
                                                               round(df_team_2['CrdY'].values[0]/df_team_2['#Games'].values[0], 2)))
            st.text("Червоні карточки (середнє): {} ({})".format(int(df_team_1['CrdR'].values[0]),
                                                            round(df_team_2['CrdR'].values[0]/df_team_2['#Games'].values[0], 2)))

        _, col221, col222, col223, col224, col225, _, col231, col232, col233, col234, col235, _ = st.columns((0.1, 1, 1, 1, 1, 1, 0.2, 1, 1, 1, 1, 1, 0.1))
        with col221:
            st.metric(label='Голи', value=int(df_team_1['Gls'].values[0]))
        with col222:
            st.metric(label='Удари', value=int(df_team_1['Sh'].values[0]))
        with col223:
            st.metric(label='Удари в площину', value=int(df_team_1['SoT'].values[0]))
        with col224:
            st.metric(label='Оффсайди', value=int(df_team_1['Off'].values[0]))
        with col225:
            st.metric(label='Фоли', value=int(df_team_1['Fls'].values[0]))

        with col231:
            st.metric(label='Голи', value=int(df_team_2['Gls'].values[0]))
        with col232:
            st.metric(label='Удари', value=int(df_team_2['Sh'].values[0]))
        with col233:
            st.metric(label='Удари в площину', value=int(df_team_2['SoT'].values[0]))
        with col234:
            st.metric(label='Оффсайди', value=int(df_team_2['Off'].values[0]))
        with col235:
            st.metric(label='Фоли', value=int(df_team_2['Fls'].values[0]))


def page_third():
    
    with st.container():
        _, col302, _, = st.columns((1, 2, 1))
        with col302:
            teams_all = data_players['Team'].unique()
            team_selected = st.selectbox('Select Team', teams_all, index=6, key=0)
            team_players_all = data_players[data_players['Team']==team_selected]['Player'].unique()
            player_selected = st.selectbox('Select Player', team_players_all, index=1, key=1)
            player_img_map = dict(zip(data_players_img['Player'], data_players_img['ImgName']))

        _, col311, _, col312, _ = st.columns((1, 1, 0.2, 1, 1))
        with col311:
            st.write('#### {}'.format(player_selected))
            player_img = player_img_map[player_selected]
            if not isinstance(player_img, str):
                st.image('img/players_img/no_name.jpeg', use_column_width=True)
            else:
                st.image(player_img_map[player_selected], width=200)

        data_player = data_players[data_players['Player']==player_selected].copy()
        with col312:
            player_min = data_player['Min'].values[0]
            st.write('#### ')
            st.text("")
            st.text("Країна: {}".format(data_player['Nation'].values[0].split(' ')[-1]))
            st.text("Позиція: {}".format(data_player['Pos'].values[0]))
            st.text("Вік: {}".format(data_player['Age'].values[0].split('-')[0]))
            st.text("Кількість матчів: {}".format(data_player['MP'].values[0]))
            st.text("Кількість матчів в основі: {}".format(data_player['Starts'].values[0]))
            st.text("Кількість хвилин: {}".format(int(player_min) if not np.isnan(player_min) else 0))

        if data_player['MP'].values[0]!=0:
            _, co321, col322, col323, col324, col325, col326, _ = st.columns((2, 1, 1, 1, 1, 1, 1, 2))
            with co321:
                st.metric(label='Голи', value=int(data_player['Gls'].values[0]))
            with col322:
                st.metric(label='Асисти', value=int(data_player['Ast'].values[0]))
            with col323:
                st.metric(label='Удари', value=int(data_player['Sh'].values[0]))
            with col324:
                st.metric(label='Удари в площину', value=int(data_player['SoT'].values[0]))
            with col325:
                st.metric(label='Оффсайди', value=int(data_player['Off'].values[0]))
            with col326:
                st.metric(label='Фоли', value=int(data_player['Fls'].values[0]))
        else:
            st.info('Вибраний гравець ще не грав у цьому сезоні.')

def page_fourth():
    st.info('Cторінка в розробці.')

def page_fifth():
    st.info('Cторінка в розробці.')


if __name__ == "__main__":
    path_player = 'data/players.pkl'
    path_img_player = 'data/players_img.pkl'
    path_img_logo = 'data/logos_img.pkl'
    path_table = 'data/table.pkl'

    data_players = pd.read_pickle(path_player)
    data_players_img = pd.read_pickle(path_img_player)
    data_logos_img = pd.read_pickle(path_img_logo)
    data_table = pd.read_pickle(path_table)

    main()

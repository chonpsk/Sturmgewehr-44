from .base import *
import requests
import datetime

def read_event_episode():
    episode_list = normalPost('/1/Episode/getUserEpisodeAll').json()['action']['event']
    for event in episode_list.values():
        for episode in event['episode_list'].values():
            if episode['show_state'] != '5':
                print (event['event_id'], episode['episode_id'])
                print (episode, '\n')
            if episode['show_state'] == '4':
                data = getData()
                data['episode_id'] = episode['episode_id']
                auto_post('/1/Episode/receiveEpisodeGift', data)
                time.sleep(0.7)
            if episode['show_state'] == '3':
                data = getData()
                data['episode_id'] = episode['episode_id']
                auto_post('/1/Episode/buyEpisode', data)
                time.sleep(0.3)
                data = getData()
                data['episode_id'] = episode['episode_id']
                auto_post('/1/Episode/receiveEpisodeGift', data)
                time.sleep(0.7)

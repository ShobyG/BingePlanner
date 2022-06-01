from wiki import find_id, find_season_episodes
import isodate
from datetime import datetime, timedelta
import numpy

class SeriesInfo:
    def __init__(self, imdb_id):
        self.series_imdb_id = imdb_id
        self.series_info = find_id(self.series_imdb_id)
        self.seasons_list = self.series_info['tvSeriesInfo']['seasons']
        self.seasons_tot = len(self.seasons_list)
        self.series_title = self.series_info['title']
        self.series_rating = self.series_info['imDbRating']
        self.series_plot = self.series_info['plot']
        self.series_image = self.series_info['image']
        self.series_runtime_data = ['0'] * (self.seasons_tot + 1)
        self.series_runtime_totals = ['0'] * (self.seasons_tot + 1)
        self.season_info = ['0'] * (self.seasons_tot + 1)
        self.season_tot_episodes = ['0'] * (self.seasons_tot + 1)
        self.season_episodes = ['0'] * (self.seasons_tot + 1)
        self.__set_series_data()

    def __set_series_data(self):
        self.series_dict = {}
        self.episode_dict = {}
        for i in range(1, len(self.series_runtime_data)):
            self.season_info[i] = find_season_episodes(self.series_imdb_id, i)
            self.season_episodes[i] = self.season_info[i]["episodes"]
            if self.season_info[i]["episodes"] is None:
                break
            self.season_tot_episodes[i] = len(self.season_info[i]["episodes"])
            self.series_runtime_data[int(i)] = [None] * (self.season_tot_episodes[i] + 1)
            for j in range(1, self.season_tot_episodes[i] + 1):
                ep_imdb_id = self.season_info[i]['episodes'][j-1]['id']
                ep_info = find_id(ep_imdb_id)
                ep_title = ep_info['title']
                ep_plot = ep_info['plot']
                try:
                    ep_season = ep_info['tvEpisodeInfo']['seasonNumber']
                    ep_number = ep_info['tvEpisodeInfo']['episodeNumber']
                    if ep_season is None:
                        break
                except Exception as e:
                    print(Exception)
                    break
                try:
                    ep_run_time = ep_info['runtimeMins']
                    if ep_run_time is None:
                        break
                except Exception as e:
                    print(Exception)
                    break
                if ep_run_time[0] == "P":
                    ep_run_time = int(isodate.parse_duration(ep_run_time).total_seconds() / 60)
                else:
                    ep_run_time = int(ep_run_time)
                self.series_runtime_data[int(i)][int(j)] = ep_run_time
                self.series_runtime_totals[int(i)] = int(self.series_runtime_totals[int(i)])
                self.series_runtime_totals[int(i)] += int(ep_run_time)
                addlist = [ep_season, ep_number, ep_title, ep_plot, ep_run_time]
                self.add_values(self.episode_dict, ep_imdb_id, addlist)
               
        addlist2 = [self.series_title, self.series_rating, self.series_plot, self.series_image, 
                                            self.seasons_tot, self.season_tot_episodes, 
                                             self.episode_dict, self.series_runtime_data, 
                                             self.series_runtime_totals, self.season_episodes]
        self.add_values(self.series_dict, self.series_imdb_id, addlist2)
  
    def add_values(self, dic, key, list_of_values):
        if key not in dic:
            dic[key] = list()
        dic[key].extend(list_of_values)
        return dic
    
    def get__series_runtime_data(self):
        return self.series_runtime_data

    def get_episode_runtime(self, season_no, episode_no):
        return self.series_runtime_data[season_no][episode_no]

    def get_season_runtime(self, season_no):
        season_runtime = 0
        series_runtime_data = self.get__series_runtime_data()
        season = series_runtime_data[season_no]

        if season_no < len(season):
            for i in range(1, len(season)):
                if season[i] is not None:
                    season_runtime += int(season[i])

        return season_runtime


if __name__ == '__main__':
    si = SeriesInfo('tt8740790')
    # si = SeriesInfo('tt4574334')
    print("test getting series runtime data")
    print(si.get__series_runtime_data())
    print("test getting episode data for season 1, episode 1")
    print(si.get_episode_runtime(1, 1))
    print("test getting runtime if no episode specified (=entire season?)")
    print(si.get_season_runtime(1))



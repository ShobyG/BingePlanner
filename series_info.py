from wiki import find_id, find_season_episodes
import isodate
from datetime import datetime, timedelta

class SeriesInfo:
    def __init__(self, imdb_id):
        print("call SeriesInfo with show id")
        self.__series_imdb_id = imdb_id
        print(self.__series_imdb_id)
        print("call Title api, get series info")
        self._series_info = find_id(self.__series_imdb_id)
        print(self._series_info)
        print("get array of number of seasons")
        self.__seasons_list = self._series_info['tvSeriesInfo']['seasons']
        print(self.__seasons_list)
        print("get title, rating, plot")
        self._series_title = self._series_info['title']
        self._series_rating = self._series_info['imDbRating']
        self._series_plot = self._series_info['plot']
        print(self._series_title)
        print(self._series_rating)
        print(self._series_plot)        
        # self.__seasons_list = (find_id(self.__series_imdb_id))['tvSeriesInfo']['seasons']
        print("create empty array of length number of seasons + 1 (index 0 stays 0, index 1 = season 1)")
        self.__series_runtime_data = ['0'] * (len(self.__seasons_list) + 1)
        print(self.__series_runtime_data)
        self.__set_series_data()

    def __set_series_data(self):
        print("for each season in array:")
        for i in range(1, len(self.__series_runtime_data)):
            print(f"Season: {i}")
            print("get season_data from SeasonEpisodes api")
            season_data = find_season_episodes(self.__series_imdb_id, i)
            print(season_data)
            print("check if episodes")
            print(season_data["episodes"])
            if season_data["episodes"] is None:
                break
            print("get number of episodes from len(season_data['episodes'])")
            no_of_episodes = len(season_data["episodes"])
            print(no_of_episodes)
            print("create array of episodes + 1, null for each episode (so 0 index is null, 1 index is ep1)")
            self.__series_runtime_data[int(i)] = [None] * (no_of_episodes + 1)
            print(f"runtime_data[{i}]: {self.__series_runtime_data[int(i)]}")
            i = int(i)
            self._s_ep_title = [[0 for x in range(no_of_episodes + 1)] for y in range(len(self.__seasons_list)+1)] 
            self._s_ep_plot = [[0 for x in range(no_of_episodes + 1)] for y in range(len(self.__seasons_list)+1)] 
            self._s_ep_season = [[0 for x in range(no_of_episodes + 1)] for y in range(len(self.__seasons_list)+1)] 
            self._s_ep_number = [[0 for x in range(no_of_episodes + 1)] for y in range(len(self.__seasons_list)+1)] 
            self._s_ep_info = [[0 for x in range(no_of_episodes + 1)] for y in range(len(self.__seasons_list)+1)] 
            print("for each episode:")
            for j in range(1, no_of_episodes+1):
                print(f"Episode: {j}")
                print("get imdb id for this episode")
                episode_imdb_id = season_data['episodes'][j-1]['id']
                print(episode_imdb_id)
                print("get all this episode info")
                self._s_ep_info[i][j] = find_id(episode_imdb_id)
                print(self._s_ep_info[i][j])
                print("save episode title, plot, season, number")
                self._s_ep_title[i][j] = self._s_ep_info[i][j]['title']
                self._s_ep_plot[i][j] = self._s_ep_info[i][j]['plot']
                self._s_ep_season[i][j] = self._s_ep_info[i][j]['tvEpisodeInfo']['seasonNumber']
                self._s_ep_number[i][j] = self._s_ep_info[i][j]['tvEpisodeInfo']['episodeNumber']
                print(self._s_ep_title[i][j])
                print(self._s_ep_plot[i][j])
                print(self._s_ep_season[i][j])
                print(self._s_ep_number[i][j])
                try:
                    print("see if there is any runtime info in Title Api for this episode id")
                    run_time = self._s_ep_info[i][j]['runtimeMins']
                    print(run_time)
                    # run_time = find_id(episode_imdb_id)['runtimeMins']
                    if run_time is None:
                        break
                except Exception as e:
                    print(Exception)
                    break
                print("parse letters from runtime string if necessary")
                if run_time[0] == "P":
                    run_time = int(isodate.parse_duration(run_time).total_seconds() / 60)
                else:
                    run_time = int(run_time)
                print(f"save runtime at runtime_data[{i}][{j}]")
                self.__series_runtime_data[int(i)][int(j)] = run_time
                print(self.__series_runtime_data[int(i)][int(j)])

        print("print the array of episode runtimes")
        print(self.__series_runtime_data)

    def get__series_data(self):
        return self.__series_runtime_data

    def get_episode_runtime(self, season_no, episode_no):
        return self.__series_runtime_data[season_no][episode_no]

    def get_season_runtime(self, season_no):
        season_runtime = 0
        series_runtime_data = self.get__series_data()
        season = series_runtime_data[season_no]

        if season_no < len(season):
            for i in range(1, len(season)):
                if season[i] is not None:
                    season_runtime += int(season[i])

        # if season_no < len(self.__series_data):
        #     season_episode_list = self.__seasons_list[season_no]
        #     for i in range(1, len(season_episode_list)):
        #         if season_episode_list[i] is not None:
        #             season_runtime += int(season_episode_list[i])
        return season_runtime


if __name__ == '__main__':
    # si = SeriesInfo('tt8740790')
    si = SeriesInfo('tt4574334')
    print(si.get__series_runtime_data())
    print("test getting episode data for season 1, episode 1")
    print(si.get_episode_runtime(1, 1))
    print("test getting runtime if no episode specified (=entire season?)")
    print(si.get_season_runtime(1))



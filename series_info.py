from wiki import find_id, find_season_episodes
import isodate
from datetime import datetime, timedelta


class SeriesInfo:
    def __init__(self, imdb_id):
        print("call SeriesInfo with show id")
        self.__series_imdb_id = imdb_id
        print("call Title api, get number of seasons")
        self.__seasons_list = (find_id(self.__series_imdb_id))['tvSeriesInfo']['seasons']
        print("create empty array of length number of seasons")
        self.__series_data = ['0'] * (len(self.__seasons_list) + 1)
        self.__set_series_data()

    def __set_series_data(self):
        print("for each season:")
        for i in self.__seasons_list:
            print("get season_data from SeasonEpisodes api")
            season_data = find_season_episodes(self.__series_imdb_id, i)
            if season_data["episodes"] is None:
                break
            print("get number of episodes from len(season_data['episodes'])")
            no_of_episodes = len(season_data["episodes"])
            print("create array of arrays for this season, empty for each episode")
            self.__series_data[int(i)] = [None] * (no_of_episodes + 1)
            print("for each episode:")
            for j in range(1, no_of_episodes+1):
                print("get imdb id for this episode")
                episode_imdb_id = season_data['episodes'][j-1]['id']
                try:
                    print("see if there is any runtime info in Title Api for this episode id")
                    run_time = find_id(episode_imdb_id)['runtimeMins']
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
                self.__series_data[int(i)][int(j)] = run_time

        print("print the array of episode runtimes")
        print(self.__series_data)

    def get__series_data(self):
        return self.__series_data

    def get_episode_runtime(self, season_no, episode_no):
        return self.__series_data[season_no][episode_no]

    def get_season_runtime(self, season_no):
        season_runtime = 0
        if season_no < len(self.__series_data):
            season_episode_list = self.__seasons_list[season_no]
            for i in range(1, len(season_episode_list)):
                if season_episode_list[i] is not None:
                    season_runtime += int(season_episode_list[i])
        return season_runtime


if __name__ == '__main__':
    si = SeriesInfo('tt8740790')
    print(si.get__series_data())
    print("test getting episode data for season 1, episode 1")
    print(si.get_episode_runtime(1, 1))
    print("test getting runtime if no episode specified (=entire season?)")
    print(si.get_season_runtime(1))


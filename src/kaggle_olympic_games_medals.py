# Import libraries
# import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns  # data visualization
from matplotlib import pyplot as plt


class KaggleOlympicGamesMedals:

    # Class level attributes
    hosts_file_name = 'olympic_hosts.csv'
    medals_file_name = 'olympic_medals.csv'
    results_file_name = 'olympic_results.csv'
    athletes_file_name = 'olympic_athletes.csv'

    # Standardized country names
    country_name_map = {
        'German Democratic Republic (Germany)': 'German Democratic Republic',
        'Federal Republic of Germany': 'Federal Republic of Germany',
        "Democratic People's Republic of Korea": 'North Korea',
        "Republic of Korea": "South Korea",
        "People's Republic of China": 'China',
        "Islamic Republic of Iran": 'Iran',
        "United States of America": 'United States'
    }

    country_code_to_std_name_map = {
        'GER': 'Germany',
        'FRG': 'Germany',
        'GDR': 'Germany',
        'CZE': 'Czech Republic',
        'TCH': 'Czech Republic',
        'IOA': 'Russia',
        'ROC': 'Russia',
        'RUS': 'Russia',
        'URS': 'Russia'
    }

    # Replaces changed discipline names
    discipline_title_map = {
        "Gymnastics Artistic": "Artistic Gymnastics",
        "Gymnastics Rhythmic": "Rhythmic Gymnastics",
        "Synchronized Swimming": "Artistic Swimming",
        "Equestrian Dressage": "Equestrian",
        "Equestrian Jumping": "Equestrian",
        "Equestrian Eventing": "Equestrian",
        "Trampoline": "Trampoline Gymnastics",
        "Cycling BMX": "Cycling BMX Racing",
        "Short Track Speed Skating": "Short Track"
    }

    pre_proc_group_cols: list[str] = [
        'discipline_title',
        'event_title',
        'event_gender',
        'medal_type',
        'participant_type',
        'participant_title',
        'country_name',
        'country_3_letter_code',
        'game_location',
        'game_season',
        'game_name',
        'game_year'
    ]

    pre_proc_agg_cols: list[str] = [
        'country_code',
        'athlete_full_name'
    ]

    def __init__(self, data_dir: str):
        """
        Initializes the object with data from the specified data directory.

        Args:
            data_dir (str): The directory path where the data files are located.

        Returns:
            None

        This function reads the data from the specified data directory and assigns it to the corresponding dataframes.
        The dataframes are:
        - df_hosts: Contains information about the Olympic hosts.
        - df_medals: Contains information about the Olympic medals.
        - df_results: Contains information about the Olympic results.
        - df_athletes: Contains information about the Olympic athletes.

        After loading the data, the function prints the message "Data Loaded".

        Note: The data files are expected to be in CSV format and have the following names:
        - hosts_file_name: The name of the file containing Olympic hosts data.
        - medals_file_name: The name of the file containing Olympic medals data.
        - results_file_name: The name of the file containing Olympic results data.
        - athletes_file_name: The name of the file containing Olympic athletes data.
        """
        self.data_dir = data_dir
        self.df_hosts = pd.read_csv(f'{data_dir}/{self.hosts_file_name}')
        self.df_medals = pd.read_csv(f'{data_dir}/{self.medals_file_name}')
        self.df_results = pd.read_csv(f'{data_dir}/{self.results_file_name}')
        self.df_athletes = pd.read_csv(f'{data_dir}/{self.athletes_file_name}')
        print('Data Loaded')

    def explore_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Explore the given DataFrame by printing information about it.

        Parameters:
            df (pd.DataFrame): The DataFrame to explore.

        Returns:
            pd.DataFrame: The first few rows of the DataFrame.

        This function takes a DataFrame as input and performs the following actions:
        1. Prints the information about the DataFrame: the number of rows, columns, data types, and memory usage.
        2. Prints the number of missing values in each column of the DataFrame.
        3. Returns the first few rows of the DataFrame.

        Note:
        - The function assumes that the input DataFrame is a pandas DataFrame.
        - The function does not modify the input DataFrame.
        """        
        print("-- Info --")
        print(df.info())
        print("\n-- Missing Info --")
        print(df.isnull().sum())
        return df.head()

    def get_hosts(self) -> pd.DataFrame:
        """
        Get the raw hosts DataFrame by returning a copy of the df_hosts attribute.

        Returns:
            pd.DataFrame: A copy of the df_hosts attribute
        """
        return self.df_hosts.copy()

    def get_hosts_with_country_codes(self) -> pd.DataFrame:
        """
        Retrieves hosts with their respective country codes by merging dataframes and updating game locations.

        Returns:
            pd.DataFrame: a DataFrame with hosts and their corresponding country codes.
        """
        df = self.get_hosts()
        df.loc[df['game_slug'] == 'melbourne-1956',
               'game_location'] = 'Australia'
        df.loc[df['game_slug'] == 'pyeongchang-2018',
               'game_location'] = 'North Korea'
        df.loc[df['game_slug'] == 'seoul-1988',
               'game_location'] = 'South Korea'
        df.loc[df['game_slug'] == 'moscow-1980',
               'game_location'] = 'Soviet Union'

        df_codes = self.get_country_name_codes()
        df = df.merge(df_codes, how='left',
                      left_on='game_location', right_on='country_name')
        df.drop(['country_name'], inplace=True, axis=1)
        df.rename(
            columns={'country_3_letter_code': 'game_country_code'}, inplace=True)
        return df

    def get_medals(self) -> pd.DataFrame:
        """
        Get the medals DataFrame by returning a copy of the df_medals attribute.

        Returns:
            pd.DataFrame: A copy of the df_medals attribute
        """
        return self.df_medals.copy()

    def _get_medals_merged(self) -> pd.DataFrame:
        """
        Merge the medals DataFrame with the hosts DataFrame based on the 'slug_game' column,
        and return the cleaned merged DataFrame.
        Internal use only.

        Returns:
            pd.DataFrame: A pandas DataFrame containing the merged and cleaned data.
        """
        return self._clean_data(self._merge_hosts(self.get_medals()))

    def get_medals_by_country(self) -> pd.DataFrame:
        """
        Get the medals DataFrame by dropping duplicate rows based on unique columns,
        and dropping unnecessary columns from the merged DataFrame.

        Returns:
            pd.DataFrame: A pandas DataFrame with medals data by country.
        """
        unique_cols: list[str] = [
            'discipline_title',
            'slug_game',
            'event_title',
            'event_gender',
            'medal_type',
            'participant_type',
            'country_3_letter_code'
        ]
        return self._get_medals_merged()\
            .drop_duplicates(subset=unique_cols)\
            .drop(columns=['participant_title', 'athlete_url', 'athlete_full_name', 'country_code'])

    def get_medals_by_std_country_name(self) -> pd.DataFrame:
        """
        Get the medals DataFrame by standardizing country names based on a mapping from country code to standard name.

        Returns:
            pd.DataFrame: A pandas DataFrame with standardized country names in the medals data.
        """
        df = self.get_medals_by_country()
        for key, value in self.country_code_to_std_name_map.items():
            df.loc[df['country_3_letter_code'] == key, 'country_name'] = value
        return df

    def get_athletes(self) -> pd.DataFrame:
        """
        Get the athletes DataFrame.

        Returns:
            pd.DataFrame: A copy of the athletes DataFrame.
        """
        return self.df_athletes.copy()

    def get_merged_athletes(self) -> pd.DataFrame:
        """
        Get the merged athletes DataFrame after cleaning and merging with host data.

        Returns:
            pd.DataFrame: A pandas DataFrame containing the merged and cleaned athletes data.
        """
        return self._clean_data(self._merge_hosts(self.get_athletes()))

    def get_results(self) -> pd.DataFrame:
        """
        Get the results DataFrame.

        Returns:
            pd.DataFrame: A copy of the results DataFrame.
        """
        return self.df_results.copy()

    def get_merged_results(self) -> pd.DataFrame:
        """
        Get the merged results DataFrame after cleaning and merging with host data.

        Returns:
            pd.DataFrame: A pandas DataFrame containing the merged and cleaned results data.
        """        
        return self._clean_data(self._merge_hosts(self.get_results()))

    def _merge_hosts(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge the given dataframe with hosts dataframes based on the 'slug_game' column

        Parameters:
            self: The instance of the class
            df (pd.DataFrame): The input DataFrame to be merged

        Returns:
            pd.DataFrame: The merged DataFrame after removing the specified columns
        """
        # Merge the given dataframe with hosts dataframes
        df_merged = df.merge(self.df_hosts, how='left',
                             left_on='slug_game', right_on='game_slug')

        # Remove merged column
        df_merged.drop(['game_slug'], inplace=True, axis=1)

        return df_merged

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans the data in the DataFrame by applying specific transformations based on column values.

        Parameters:
            df (pd.DataFrame): The input DataFrame to be cleaned.

        Returns:
            pd.DataFrame: The cleaned DataFrame after applying the transformations.
        """
        if 'athlete_full_name' in df.columns:
            df['athlete_full_name'] = df['athlete_full_name'].str.title()

        if 'country_name' in df.columns:
            df['country_name'] = df['country_name'].replace(
                self.country_name_map)

        if 'discipline_title' in df.columns:
            df['discipline_title'] = df['discipline_title'].replace(
                self.discipline_title_map)
            if 'event_title' in df.columns:
                self._fix_discipline_events(df)

        return df

    def _clean_event_title(self, et: str) -> str:
        if et.startswith("Women's"):
            et = et.replace("Women's", '')+' women'
        elif et.startswith("Men's"):
            et = et.replace("Men's", '')+' men'
        return et.lower().strip()

    def _fix_discipline_events(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fixes the discipline and event titles in the given DataFrame.

        Parameters:
            df (pd.DataFrame): The DataFrame containing the data.

        Returns:
            pd.DataFrame: The DataFrame with the fixed discipline and event titles.
        """
        # fix some disciplines and events
        df.loc[df['event_title'] == 'Baseball',
               'discipline_title'] = 'Baseball'
        df.loc[df['event_title'] == 'Softball',
               'discipline_title'] = 'Softball'
        df.loc[df['event_title'] == 'Baseball', 'event_title'] = 'baseball men'
        df.loc[df['event_title'] == 'Softball',
               'event_title'] = 'softball women'

        df.loc[df['event_title'] == 'rugby-7 men',
               'discipline_title'] = 'Rugby Sevens'
        df.loc[df['event_title'] == 'rugby-7 women',
               'discipline_title'] = 'Rugby Sevens'
        df.loc[df['event_title'] == 'rugby-7 men', 'event_title'] = 'men'
        df.loc[df['event_title'] == 'rugby-7 women', 'event_title'] = 'women'
        df['event_title'] = df['event_title'].apply(lambda et: self._clean_event_title(et))
        return df

    def pre_process_medal_counts(self, df: pd.DataFrame):
        """
        The dataset contains two different rows for both winners in a team competition
        that consists of two persons, but it is one medal in total. For example, you
        can check the Tennis Doubles Men competition. Let's split the dataset into
        parts, group those team competitions, and join data again.

        Pre-processes the medal counts data by separating athletes and game teams,
        grouping game teams by specified columns, and aggregating athlete full names
        and country codes. The function takes in a pandas DataFrame as input and
        returns a pre-processed DataFrame.

        Parameters:
        - df (pd.DataFrame): The input DataFrame containing medal counts data.

        Returns:
        - pd.DataFrame: The pre-processed DataFrame with separate athlete and game team
          data, aggregated athlete full names and country codes, and concatenated with
          the original athlete data.
        """
        df_athlete = df[df['participant_type'] == 'Athlete']
        df_team = df[df['participant_type'] == 'GameTeam']
        df_team_a = df_team[df_team['athlete_full_name'].isna()]
        df_team_b: pd.DataFrame = df_team[df_team['athlete_full_name'].notna()]\
            .groupby(self.pre_proc_group_cols)[self.pre_proc_agg_cols].agg(lambda x: set(x))\
            .reset_index()

        df_team_b['country_code'] = df_team_b['country_code'].apply(
            lambda x: list(x)[0])

        df_team_b['athlete_full_name'] = df_team_b['athlete_full_name'].apply(
            lambda x: list(x))

        return pd.concat([df_team_a, df_team_b, df_athlete], axis=0).reset_index(drop=True)

    def get_discipline_game_heatmap(self, df: pd.DataFrame, season: str) -> pd.DataFrame:
        """
        Generates a heatmap DataFrame based on the input DataFrame filtered by a specific season.

        Parameters:
        - df (pd.DataFrame): The input DataFrame containing data of various disciplines and game years.
        - season (str): The specific season to filter the data by.

        Returns:
        - pd.DataFrame: A heatmap DataFrame representing the count of medals in each discipline
        over the game years.
        """
        # Filter by season and reset the index
        # Group by discipline and game year and count the number of medals
        df_heatmap = df[df['game_season'] == season].reset_index(drop=True)
        df_heatmap = df_heatmap.groupby(
            ['discipline_title', 'game_year']
        )['participant_type'].count().reset_index()

        # Pivot the dataframe with discipline_title values as rows (index) and game_year values as columns
        df_heatmap = df_heatmap.pivot(
            index='discipline_title', columns='game_year', values='participant_type')
        df_heatmap[df_heatmap > 0] = 1
        column_list = list(df_heatmap.columns)
        most_current_game_year = column_list[-1]

        # Sort the heatmap so that disciplines with the most recent game year are at the top
        disciplines_current = df_heatmap[df_heatmap[most_current_game_year] == 1].sort_values(
            column_list)
        disciplines_older = df_heatmap[df_heatmap[most_current_game_year] != 1].sort_values(
            column_list)
        df_heatmap = pd.concat([disciplines_current, disciplines_older])
        
        # Format the index and columns of the heatmap
        df_heatmap.columns = [str(col)[:-2]+'\n'+str(col)[-2:]
                              for col in column_list]
        df_heatmap.index = [idx.replace(' ', '\n', 1)
                            for idx in df_heatmap.index]
        return df_heatmap

    def _sort_game_names(self, game_name_list: list[str]) -> list[str]:
        """
        Sorts the list of game names in ascending order based on the last word (year) in each name.

        Example:
        Input: ['Sydney 2000', 'Atlanta 1996', 'Beijing 2008', 'Athens 2004']
        Output: ['Atlanta 1996', 'Sydney 2000', 'Athens 2004', 'Beijing 2008'

        Parameters:
            game_name_list (list[str]): A list of game names to be sorted.

        Returns:
            list[str]: A sorted list of game names.
        """
        game_name_tuple_split = [
            (' '.join(i.split(' ')[:-1]), i.split(' ')[-1]) for i in game_name_list]
        game_name_tuple_sorted = sorted(
            game_name_tuple_split, key=lambda x: x[1])
        game_name_list_sorted = [' '.join(i) for i in game_name_tuple_sorted]
        return game_name_list_sorted

    def get_country_medal_heatmap(self, df: pd.DataFrame, country: str) -> pd.DataFrame:
        """
        Generates a heatmap DataFrame based on the input DataFrame filtered by a specific country.

        Parameters:
            - df (pd.DataFrame): The input DataFrame containing data of various disciplines and participant types.
            - country (str): The specific country to filter the data by.

        Returns:
            - pd.DataFrame: A heatmap DataFrame representing the count of medals in each discipline
            over the game names.
        """
        # Get data for given country
        df_medal = df[df['country_name'] == country]

        # Group by game_name and discipline_title and count number of medals
        df_medal = df_medal.groupby(
            ['game_name', 'discipline_title']
        )['participant_type'].count().reset_index()

        # Reorient dataframe with discipline_title values as rows (index) and game_name values as columns via pivot
        df_medal = df_medal.pivot(
            index='discipline_title', columns='game_name', values='participant_type')

        # Reorder columns by sorted game_name column values by year ascending
        df_medal = df_medal[self._sort_game_names(list(df_medal.columns))]

        # Adjust column names depending on number of columns
        if len(list(df_medal.columns)) < 10:
            df_medal.columns = [col.replace(
                ' ', '\n') for col in df_medal.columns]
        else:
            df_medal.columns = [col.split(' ')[-1] for col in df_medal.columns]

        # Calculate totals by row and overall total
        df_medal['Total'] = df_medal.sum(axis=1)
        df_medal.loc['Total'] = df_medal.sum()

        return df_medal

    def get_country_discipline_gender_medal_heatmap(
            self,
            df: pd.DataFrame,
            season: str,
            country: str,
            discipline: str,
            gender: str) -> pd.DataFrame:
        """
        This function generates a heatmap DataFrame of medals for a specific country, discipline,
        and gender in a given season.

        Parameters:
            df: pd.DataFrame - the dataframe containing the data
            season: str - the season for which the heatmap is generated
            country: str - the country for which the heatmap is generated
            discipline: str - the discipline for which the heatmap is generated
            gender: str - the gender for which the heatmap is generated

        Returns:
            pd.DataFrame - the heatmap of medals for the specified country, discipline, and gender
        """
        df_discipline = df[
            (df['game_season'] == season) &
            (df['country_name'] == country) &
            (df['discipline_title'] == discipline) &
            (df['event_gender'] == gender)
        ].reset_index(drop=True)

        # Group by game_name and event_title and count number of medals
        df_discipline = df_discipline.groupby(
            ['game_name', 'event_title']
        )['participant_type'].count().reset_index()

        # Reorient dataframe with event_title values as rows (index) and game_name values as columns via pivot
        df_discipline = df_discipline.pivot(
            index='event_title', columns='game_name', values='participant_type')

        # Reorder columns by sorted game_name column values by year ascending
        df_discipline = df_discipline[self._sort_game_names(
            list(df_discipline.columns))]
        df_discipline.sort_index(ascending=True, inplace=True)

        # Adjust column names depending on number of columns
        if len(list(df_discipline.columns)) < 10:
            df_discipline.columns = [col.replace(
                ' ', '\n') for col in df_discipline.columns]
        else:
            df_discipline.columns = [
                col.split(' ')[-1] for col in df_discipline.columns]

        # Calculate totals by row and overall total
        df_discipline['Total'] = df_discipline.sum(axis=1)
        df_discipline.loc['Total'] = df_discipline.sum()

        return df_discipline

    def plot_discipline_games_heatmap(self, df: pd.DataFrame, title: str, size=(16, 16), save=False):
        """
        Plots a heatmap of the disciplines contested at a specific Olympic Games.
        The DataFrame should have columns 'game_name' and 'discipline_title' and rows representing participants.

        Parameters:
            df (pd.DataFrame): The DataFrame containing the data to be plotted.
            title (str): The title of the Olympic Games.
            size (tuple, optional): The size of the figure. Defaults to (16, 16).
            save (bool, optional): Whether to save the plot as an image. Defaults to False.

        Returns:
            None
        """
        plt.figure(figsize=size)
        ax = sns.heatmap(df, annot=False, cbar=False,
                         linewidths=0.8, linecolor='lightgrey',
                         square=True, cmap='Spectral')
        ax.set_title(f'Disciplines Contested at the {title} Olympic Games', size=18)
        ax.xaxis.tick_top()
        ax.spines[['bottom', 'right']].set_visible(True)
        plt.tight_layout()
        if save:
            plt.savefig(f'{title.lower()}_games.png', dpi=200)
        plt.show()

    def plot_country_medal_heatmap(self, df: pd.DataFrame, country: str, season: str, figsize=(16, 16), save=False):
        """
        Create a heatmap with annotations representing the medals won by a specific country in a given season.

        Parameters:
            df (pd.DataFrame): The DataFrame containing the medal data.
            country (str): The name of the country for which the medals heatmap is generated.
            season (str): The season for which the medals heatmap is generated.
            figsize (tuple, optional): The size of the figure for the heatmap. Defaults to (16, 16).
            save (bool, optional): A flag indicating whether to save the generated heatmap as an image.
            Defaults to False.
        """
        # Create the heatmap with annotations
        plt.figure(figsize=figsize)
        ax = sns.heatmap(df, annot=True, fmt='g', linewidths=0.8, cmap='coolwarm')
        ax.set_title(f'{country} {season} Medals', size=18)
        ax.xaxis.tick_top()
        plt.tight_layout()
        if save:
            plt.savefig(f'{country.lower()}_{season.lower()}_medals.png', dpi=200)
        plt.show()

    def plot_country_discipline_gender_medal_heatmap(
            self,
            df: pd.DataFrame,
            season: str,
            country: str,
            discipline: str,
            gender: str,
            figsize=(16, 16),
            save=False):

        plt.figure(figsize=figsize)
        ax = sns.heatmap(df, annot=True, fmt='g', linewidths=0.8, cmap='coolwarm')
        ax.set_title(f'{country} {season} {discipline} Medals - {gender}', size=22)
        ax.xaxis.tick_top()
        plt.tight_layout()
        if save:
            plt.savefig(f'{country.lower()}_{season.lower()}_{discipline.lower()}_{gender.lower()}_medals.png', dpi=200)
        plt.show()

    def get_country_name_codes(self) -> pd.DataFrame:
        """
        Returns a DataFrame containing the country name and code for each country in the medals dataset.

        :return: pd.DataFrame
        """
        df = self.get_medals_by_country(
        )[['country_name', 'country_3_letter_code']].set_index('country_name').sort_index()

        # Drop duplicate country codes
        return df.drop_duplicates(['country_3_letter_code']).reset_index()

# pylint: disable=invalid-name
"""This is a twitter scrapper class given a CSV file with users, 
names and starting date with twint API.
"""

import logging
import os
import pandas as pd
import numpy as np

import twint as tw

from function_validators import (
    check_dataframe_integrity,
    check_date_integrity_dataframe,
)

__all__ = ["TwitterScrapper"]


class TwitterScrapper:
    """Given a set of parameters and CSV file with twitter usernames and dates,
    This class performs tweets scrapping processes using twint and saves the
    results into another file.
    """

    FILE_NAME = "user_file"
    USER_COLUMNS_ACCEPTED = ["Usuario", "usuario", "User", "user"]
    SAVING_EXTENSION = "file_to_save_extension"
    DEFAULT_EXTENSION = ".npy"
    ENCODING_FIELD = "encoding"
    DEFAULT_ENCODING = "utf-8"
    OUT_FILE = "file_to_save_name"
    DEFAULT_OUT_FILE = "results.npy"

    def __init__(self, params: dict):
        self.params = params
        self.user_file = params.get(self.FILE_NAME, None)
        self.file_to_save = params.get(self.OUT_FILE, self.DEFAULT_OUT_FILE)
        self.encoding = params.get(self.ENCODING_FIELD, self.DEFAULT_ENCODING)

        self.users = pd.read_csv(self.user_file)
        self.users.index = range(len(self.users))

    def preprocess(self, df: pd.Dataframe, f_out: str) -> pd.DataFrame:
        """Checks if there is a user name. If no account found,
        the registry will be saved at a file with missing accounts.

        Args:
            df (DataFrame): Users initial DataFrame
            f_out (str): out filename with only existing accounts

        Returns:
            pd.DataFrame:only existing accounts registries.
        """
        missing = df[df["Usuario"].isnull() is True]
        df = df[df["Usuario"].isnull() is False]
        name = f_out[15:-4] + "_missing.csv"
        missing.to_csv("Usuarios/" + name)
        return df

    @check_dataframe_integrity
    @check_date_integrity_dataframe
    def get_replies(self, date_since: str, username: str) -> pd.DataFrame:
        """Fetches replies with twint API

        Args:
            date_since (str): start date to parse from
            username (str): username to fetch from Twitter

        Returns:
            pd.DataFrame: Dataframe with replies
        """
        replies = tw.Config()
        replies.Since = date_since
        replies.Pandas = True
        replies.To = username
        replies.Hide_output = True
        tw.run.Search(replies)
        return tw.storage.panda.Tweets_df

    def save_replies(self, file: str, filename: str, encoding: str) -> pd.DataFrame:
        """This calls the replies fetching and saves the replies into CSV.

        Args:
            file (str): name of file to get registries
            filename (str): output file name
            encoding (str): expected encoding, defaults to UTF-8

        Returns:
            pd.DataFrame: Outpus the replies within a DataFrame
        """
        columnas = file.columns
        data = pd.DataFrame(columns=columnas)

        _, extension = os.path.splitext(filename)
        for person in file.index:
            logging.info("Retrieving replies to: {person}")
            date_from = file.loc[person]["Fecha de inicio"]
            username = file.iloc[person][2][1:]
            data = data.append(self.get_replies(date_from, username))

        if extension == self.DEFAULT_EXTENSION:
            np.save(filename, data.values)
        else:
            data.to_csv(filename, encoding=encoding)

    @check_dataframe_integrity
    def main_loop(self):
        """Main loog pre-processes a file and gets the replies within a new file."""
        logging.info(f"Leyendo {self.user_file}")
        existing_users = self.preprocess(self.users, self.file_to_save)
        self.save_replies(existing_users, self.file_to_save, self.encoding)
